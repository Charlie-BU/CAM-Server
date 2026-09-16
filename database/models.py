from sqlalchemy import (
    inspect,
    Table,
    Column,
    String,
    Integer,
    Boolean,
    ForeignKey,
    Enum,
    Text,
    DateTime,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone

from .enums import (
    HttpMethod,
    ApiLevel,
    ParamLocation,
    ParamType,
    UserRole,
    UserLevel,
)
from bcrypt import hashpw, gensalt, checkpw

Base = declarative_base()
# 数据库表名和列名的命名规范
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
Base.metadata.naming_convention = naming_convention


# 可序列化Mixin基类，提供toJson方法将模型实例转换为JSON
class SerializableMixin:
    def toJson(self, include=None, exclude=["password"], include_relations=False):
        include = set(include) if include else None
        exclude = set(exclude) if exclude else set()
        mapper = inspect(self.__class__)
        if not mapper:
            return {}

        data = {}
        for column in mapper.columns:
            name = column.key
            if include:
                if name not in include:
                    continue
                # 若有 include，则要检查关系是否在 include 中
                for rel in mapper.relationships:
                    if rel.key in include:
                        value = getattr(self, rel.key)
                        data[rel.key] = value.toJson() if value else None
                        continue
            if name in exclude:
                continue
            value = getattr(self, name)
            if isinstance(value, datetime):
                value = value.isoformat()
            data[name] = value

        if include_relations:
            for rel in mapper.relationships:
                if rel.key in exclude:
                    continue
                value = getattr(self, rel.key)
                if value is None:
                    data[rel.key] = None
                elif isinstance(value, list):
                    data[rel.key] = [v.toJson() for v in value]
                else:
                    data[rel.key] = value.toJson()
        return data


# ---- 用户-服务关联表 ----
user_service_link = Table(
    "user_service_link",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("service_id", Integer, ForeignKey("service.id"), primary_key=True),
)


# ---- 用户表 ----
class User(Base, SerializableMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    services = relationship(
        "Service", secondary=user_service_link, back_populates="maintainers"
    )
    auth_identities = relationship(
        "UserAuthIdentity",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    username = Column(String(64), unique=True, nullable=False, index=True)
    password = Column(String(128), nullable=True)
    nickname = Column(String(64), nullable=True, index=True)
    email = Column(String(128), nullable=True, unique=True)
    role = Column(Enum(UserRole), default=UserRole.GUEST)
    level = Column(Enum(UserLevel), default=UserLevel.L4)
    created_at = Column(DateTime, server_default=func.now())

    @staticmethod
    def hashPassword(password):
        hashed = hashpw(password.encode("utf-8"), gensalt())
        return hashed.decode("utf-8")

    def checkPassword(self, password):
        if not self.password:
            return False
        return checkpw(password.encode("utf-8"), self.password.encode("utf-8"))

    # 自定义toJson方法，包含密码和第三方身份信息
    def toJson(self, include=None, exclude=["password"], include_relations=False):
        data = super().toJson(include, exclude, include_relations)
        data["has_password"] = bool(self.password)
        data["auth_providers"] = sorted(
            {identity.provider for identity in self.auth_identities}
        )
        return data

    def __repr__(self):
        return f"<User {self.username}>"


# ---- 用户第三方身份表 ----
class UserAuthIdentity(Base, SerializableMixin):
    __tablename__ = "user_auth_identity"
    __table_args__ = (
        UniqueConstraint(
            "provider",
            "provider_subject",
            name="uq_user_auth_identity_provider_subject",
        ),
        UniqueConstraint(
            "user_id",
            "provider",
            name="uq_user_auth_identity_user_provider",
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer,
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user = relationship("User", back_populates="auth_identities")
    provider = Column(String(32), nullable=False)
    provider_subject = Column(String(255), nullable=False)
    provider_email = Column(String(128), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    last_login_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self):
        return f"<UserAuthIdentity {self.provider}:{self.user_id}>"


# ---- 服务表 ----
class Service(Base, SerializableMixin):
    __tablename__ = "service"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    owner = relationship("User", backref="owned_services")
    maintainers = relationship(
        "User", secondary=user_service_link, back_populates="services"
    )

    service_uuid = Column(
        String(64), unique=True, nullable=False, index=True
    )  # 只存放一个服务的最新版本，历史版本存在ServiceIteration表中
    version = Column(String(32), nullable=False, index=True)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    # 软删除
    is_deleted = Column(Boolean, default=False, index=True)
    deleted_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Service {self.service_uuid}:{self.version}>"


# ---- 服务迭代表（存储每个服务的每个历史版本和最新版本，最新版本和Service保持一致） ----
class ServiceIteration(Base, SerializableMixin):
    __tablename__ = "service_iteration"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 每个 iteration 对应 service 的一次完整快照
    service_id = Column(Integer, ForeignKey("service.id"), nullable=False)
    service = relationship("Service", backref="iterations")
    # 迭代创建人
    creator_id = Column(Integer, ForeignKey("user.id"))
    creator = relationship("User", backref="created_iterations")

    version = Column(
        String(32), nullable=True
    )  # 发布前可为空，发布后最新迭代与 service.version 对齐
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    # 是否已发布
    is_committed = Column(Boolean, default=False)

    def __repr__(self):
        return f"<ServiceIteration {self.service_id}:{self.version}>"


# ---- 接口分类表 ----
class ApiCategory(Base, SerializableMixin):
    __tablename__ = "api_category"
    # API路径和方法组合唯一约束
    __table_args__ = (
        UniqueConstraint("service_id", "name", name="uq_service_category_name"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey("service.id"), nullable=False, index=True)
    service = relationship("Service", backref="api_categories")

    name = Column(String(64), nullable=False, index=True)
    description = Column(Text)

    def __repr__(self):
        return f"<ApiCategory {self.name}>"


# ---- 接口表 ----
class Api(Base, SerializableMixin):
    __tablename__ = "api"
    # API路径和方法组合唯一约束
    __table_args__ = (
        UniqueConstraint("service_id", "method", "path", name="uq_api_method_path"),
    )
    # API名称和方法组合唯一约束
    __table_args__ = (
        UniqueConstraint("service_id", "method", "name", name="uq_api_method_name"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(Integer, ForeignKey("service.id"), nullable=False, index=True)
    service = relationship("Service", backref="apis")
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    owner = relationship("User", backref="apis")
    category_id = Column(
        Integer, ForeignKey("api_category.id"), nullable=True, index=True
    )
    category = relationship("ApiCategory", backref="apis")

    name = Column(String(128), nullable=False)
    method = Column(Enum(HttpMethod), nullable=False, index=True)
    path = Column(String(256), nullable=False, index=True)
    description = Column(Text)
    level = Column(Enum(ApiLevel), default=ApiLevel.P4)  # P0/P1/P2/P3/P4
    is_enabled = Column(Boolean, default=True)  # 是否启用
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Api {self.name} [{self.method.value}] {self.path}>"


# ---- 请求参数 ----
class RequestParam(Base, SerializableMixin):
    __tablename__ = "request_param"

    id = Column(Integer, primary_key=True, autoincrement=True)
    api_id = Column(
        Integer, ForeignKey("api.id", ondelete="CASCADE"), nullable=False, index=True
    )  # 级联删除：删除api时，删除所有相关的param
    api = relationship("Api", backref="request_params")

    name = Column(String(64), nullable=False, index=True)
    location = Column(
        Enum(ParamLocation), nullable=False
    )  # query/path/header/cookie/body
    type = Column(
        Enum(ParamType), nullable=False
    )  # string/int/double/boolean/array/object/binary
    required = Column(Boolean, default=False)
    # 与 required 独立：参数存在时是否允许传 JSON null。
    nullable = Column(Boolean, nullable=False, default=False, server_default="false")
    default_value = Column(String(256), nullable=True)
    description = Column(Text)
    example = Column(String(256))

    # 如果是array类型，需要规定元素类型
    array_child_type = Column(Enum(ParamType), nullable=True)
    # 如果存在是object类型，需要有子参数（这里以子参数视角）
    parent_param_id = Column(
        Integer,
        ForeignKey("request_param.id", ondelete="CASCADE"),
        nullable=True,  # 级联删除：删除param时，删除所有相关的子param
    )
    parent_param = relationship(
        "RequestParam", backref="child_params", remote_side=[id]
    )
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<RequestParam {self.name} ({self.location.value})>"


# ---- 响应参数 ----
class ResponseParam(Base, SerializableMixin):
    __tablename__ = "response_param"

    id = Column(Integer, primary_key=True, autoincrement=True)
    api_id = Column(
        Integer, ForeignKey("api.id", ondelete="CASCADE"), nullable=False, index=True
    )  # 级联删除：删除api时，删除所有相关的param
    api = relationship("Api", backref="response_params")

    status_code = Column(Integer, nullable=False)
    name = Column(String(64), nullable=False, index=True)
    type = Column(Enum(ParamType), nullable=False)
    required = Column(Boolean, default=False)
    nullable = Column(Boolean, nullable=False, default=False, server_default="false")
    description = Column(Text)
    example = Column(String(256))

    # 如果是array类型，需要规定元素类型
    array_child_type = Column(Enum(ParamType), nullable=True)
    # 如果存在是object类型，需要有子参数（这里以子参数视角）
    parent_param_id = Column(
        Integer, ForeignKey("response_param.id", ondelete="CASCADE"), nullable=True
    )  # 级联删除：删除param时，删除所有相关的子param
    parent_param = relationship(
        "ResponseParam", backref="child_params", remote_side=[id]
    )
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<ResponseParam {self.name} ({self.status_code})>"


# ---- 接口草稿表 ----
class ApiDraft(Base, SerializableMixin):
    __tablename__ = "api_draft"
    # API路径和方法组合唯一约束
    __table_args__ = (
        UniqueConstraint(
            "service_iteration_id", "method", "path", name="uq_api_method_path_draft"
        ),
    )
    # API名称和方法组合唯一约束
    __table_args__ = (
        UniqueConstraint(
            "service_iteration_id", "method", "name", name="uq_api_method_name_draft"
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_iteration_id = Column(
        Integer, ForeignKey("service_iteration.id"), nullable=False, index=True
    )
    service_iteration = relationship("ServiceIteration", backref="api_drafts")
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False, index=True)
    owner = relationship("User", backref="api_drafts")
    category_id = Column(
        Integer, ForeignKey("api_category.id"), nullable=True, index=True
    )
    category = relationship("ApiCategory", backref="api_drafts")

    name = Column(String(128), nullable=False)
    method = Column(Enum(HttpMethod), nullable=False, index=True)
    path = Column(String(256), nullable=False, index=True)
    description = Column(Text)
    level = Column(Enum(ApiLevel), default=ApiLevel.P4)  # P0/P1/P2/P3/P4
    is_enabled = Column(Boolean, default=True)  # 是否启用
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<ApiDraft {self.name} [{self.method.value}] {self.path}>"


# ---- 请求参数草稿 ----
class RequestParamDraft(Base, SerializableMixin):
    __tablename__ = "request_param_draft"

    id = Column(Integer, primary_key=True, autoincrement=True)
    api_draft_id = Column(
        Integer,
        ForeignKey("api_draft.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )  # 级联删除：删除draft时，删除所有相关的param
    api_draft = relationship("ApiDraft", backref="request_params")

    name = Column(String(64), nullable=False, index=True)
    location = Column(
        Enum(ParamLocation), nullable=False
    )  # query/path/header/cookie/body
    type = Column(
        Enum(ParamType), nullable=False
    )  # string/int/double/boolean/array/object/binary
    required = Column(Boolean, default=False)
    nullable = Column(Boolean, nullable=False, default=False, server_default="false")
    default_value = Column(String(256), nullable=True)
    description = Column(Text)
    example = Column(String(256))

    # 如果是array类型，需要规定元素类型
    array_child_type = Column(Enum(ParamType), nullable=True)
    # 如果存在是object类型，需要有子参数（这里以子参数视角）
    parent_param_id = Column(
        Integer, ForeignKey("request_param_draft.id", ondelete="CASCADE"), nullable=True
    )  # 级联删除：删除param时，删除所有相关的子param
    parent_param = relationship(
        "RequestParamDraft", backref="child_params", remote_side=[id]
    )
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<RequestParamDraft {self.name} ({self.location.value})>"


# ---- 响应参数草稿 ----
class ResponseParamDraft(Base, SerializableMixin):
    __tablename__ = "response_param_draft"

    id = Column(Integer, primary_key=True, autoincrement=True)
    api_draft_id = Column(
        Integer,
        ForeignKey("api_draft.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )  # 级联删除：删除draft时，删除所有相关的param
    api_draft = relationship("ApiDraft", backref="response_params")

    status_code = Column(Integer, nullable=False)
    name = Column(String(64), nullable=False, index=True)
    type = Column(Enum(ParamType), nullable=False)
    required = Column(Boolean, default=False)
    nullable = Column(Boolean, nullable=False, default=False, server_default="false")
    description = Column(Text)
    example = Column(String(256))

    # 如果是array类型，需要规定元素类型
    array_child_type = Column(Enum(ParamType), nullable=True)
    # 如果存在是object类型，需要有子参数（这里以子参数视角）
    parent_param_id = Column(
        Integer,
        ForeignKey("response_param_draft.id", ondelete="CASCADE"),
        nullable=True,
    )  # 级联删除：删除param时，删除所有相关的子param
    parent_param = relationship(
        "ResponseParamDraft", backref="child_params", remote_side=[id]
    )
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<ResponseParamDraft {self.name} ({self.status_code})>"


# ---- 子应用配置表 ----
class SubApplication(Base, SerializableMixin):
    """微前端子应用配置"""

    __tablename__ = "sub_application"
    id = Column(
        Integer, primary_key=True,
        comment="子应用配置主键。",
    )
    app_key = Column(
        String(64), unique=True, nullable=False,
        comment="子应用唯一标识，创建后不可修改，用于目录识别。",
    )
    name_zh = Column(
        String(128), nullable=False,
        comment="子应用中文名称，用于中文界面展示。",
    )
    name_en = Column(
        String(128), nullable=False,
        comment="子应用英文名称，用于英文界面展示。",
    )
    description_zh = Column(
        Text, nullable=False, default="",
        comment="子应用中文说明，可为空。",
    )
    description_en = Column(
        Text, nullable=False, default="",
        comment="子应用英文说明，可为空。",
    )
    icon_url = Column(
        String(2048), nullable=False, default="",
        comment="应用图标地址，支持 HTTP(S) URL 或基座根相对路径，可为空。",
    )
    app_type = Column(
        String(16), nullable=False,
        comment="接入类型：federation 表示远程组件，iframe 表示嵌入网页。",
    )
    route_path = Column(
        String(128), unique=True, nullable=False,
        comment="子应用在基座中的唯一顶层路由路径，例如 /cam。",
    )
    frontend_url = Column(
        String(2048), nullable=False,
        comment="前端入口地址：Federation 的 manifest 或 remote entry URL，或 iframe 网页 URL。",
    )
    remote_name = Column(
        String(64), nullable=False, default="",
        comment="Federation 远程容器名称；iframe 应用为空。",
    )
    exposed_module = Column(
        String(128), nullable=False, default="",
        comment="Federation 导出模块路径，例如 ./App；iframe 应用为空。",
    )
    backend_url = Column(
        String(2048), nullable=False, default="",
        comment="子应用后端服务根地址，由浏览器直接访问；无后端或 iframe 应用为空。",
    )
    sort_order = Column(
        Integer, nullable=False, default=0,
        comment="展示排序值，数值越小越靠前，相同值按主键排序。",
    )
    enabled = Column(
        Boolean, nullable=False, default=True,
        comment="是否启用应用；停用后不进入基座运行目录。",
    )
    show_in_menu = Column(
        Boolean, nullable=False, default=True,
        comment="是否显示在侧导菜单中；隐藏菜单不影响已启用应用的直接路由访问。",
    )
    require_login = Column(
        Boolean, nullable=False, default=True,
        comment="通过基座访问子应用是否需要登录。",
    )
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False,
        comment="配置创建时间，包含时区信息。",
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,
        comment="配置最后更新时间，包含时区信息。",
    )
    created_by = Column(
        Integer, ForeignKey("user.id"), nullable=True,
        comment="创建配置的用户 ID，关联用户表；手动初始化时可为空。",
    )
    updated_by = Column(
        Integer, ForeignKey("user.id"), nullable=True,
        comment="最后修改配置的用户 ID，关联用户表；手动初始化时可为空。",
    )
    deleted_at = Column(
        DateTime(timezone=True), nullable=True,
        comment="软删除时间；为空表示未删除，删除后保留原有标识和路径占用。",
    )

    def __repr__(self):
        return f"<SubApplication {self.app_key} ({self.name_zh})>"
