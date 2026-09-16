"""子应用配置校验、目录投影和事务操作。"""
from datetime import datetime, timezone
import re
from urllib.parse import urlsplit, urlunsplit
from sqlalchemy import or_
from sqlalchemy.orm import Session
from database.models import User, SubApplication


class ApplicationError(Exception):
    def __init__(self, code: str, status: int = 400):
        """初始化子应用业务异常及 HTTP 状态码。"""
        super().__init__(code)
        self.code = code
        self.status = status


FIELDS = (
    "app_key",
    "name_zh",
    "name_en",
    "description_zh",
    "description_en",
    "icon_url",
    "app_type",
    "route_path",
    "frontend_url",
    "remote_name",
    "exposed_module",
    "backend_url",
    "sort_order",
    "enabled",
    "show_in_menu",
    "require_login",
)
DEFAULTS = {
    "description_zh": "",
    "description_en": "",
    "icon_url": "",
    "remote_name": "",
    "exposed_module": "",
    "backend_url": "",
    "sort_order": 0,
    "enabled": True,
    "show_in_menu": True,
    "require_login": True,
}
# 不允许在 route_path 中使用保留的字符串
RESERVED = {
    "api", "sub-applications", "health", "assets", "src",
    "node_modules", "__cdi", "sub-app-icons",
}


def _subApplicationRequireAuth(db: Session, user_id: int | None) -> User:
    """检查用户身份及 L0 管理权限。"""
    user = db.get(User, user_id) if user_id is not None else None
    if user is None:
        raise ApplicationError("UNAUTHORIZED", 401)
    if user.level.value != 0:
        raise ApplicationError("FORBIDDEN", 403)
    return user


def _subApplicationNormalizeUrl(
    value: str, optional: bool = False, icon: bool = False
) -> str:
    """校验并规范化应用地址或图标地址。"""
    if not isinstance(value, str):
        raise ApplicationError("INVALID_URL")
    value = value.strip()
    if not value and optional:
        return ""
    if len(value) > 2048 or any(ord(c) < 32 for c in value) or "\\" in value:
        raise ApplicationError("INVALID_URL")
    if (
        icon
        and value.startswith("/")
        and not value.startswith("//")
        and ".." not in value.split("/")
    ):
        return value
    try:
        url = urlsplit(value)
        port = url.port
        if (
            url.scheme not in ("http", "https")
            or not url.hostname
            or url.username
            or url.password
            or url.fragment
            or url.query
        ):
            raise ValueError()
        if port is not None and not 0 < port < 65536:
            raise ValueError()
        if any(segment in (".", "..") for segment in url.path.split("/")):
            raise ValueError()
        return urlunsplit((url.scheme, url.netloc, url.path.rstrip("/"), "", ""))
    except ValueError:
        raise ApplicationError("INVALID_URL") from None


def _subApplicationValidate(values: dict) -> dict:
    """校验子应用配置字段并补齐默认值。"""
    if not isinstance(values, dict) or set(values) - set(FIELDS):
        raise ApplicationError("INVALID_FIELDS")
    data = {**DEFAULTS, **values}
    for key in ("app_key", "name_zh", "name_en", "app_type", "route_path", "frontend_url"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ApplicationError("REQUIRED_FIELD")
        data[key] = data[key].strip()
    if not re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", data["app_key"]):
        raise ApplicationError("INVALID_KEY")
    for key, limit in (
        ("name_zh", 128),
        ("name_en", 128),
        ("description_zh", 4000),
        ("description_en", 4000),
    ):
        if not isinstance(data[key], str) or len(data[key]) > limit:
            raise ApplicationError("INVALID_FIELDS")
    path = data["route_path"]
    if (
        not path.startswith("/")
        or len(path) > 128
        or not re.fullmatch(r"/[a-z0-9_-]+(?:/[a-z0-9_-]+)*", path)
        or path.split("/")[1].lower() in RESERVED
    ):
        raise ApplicationError("INVALID_ROUTE")
    if data["app_type"] not in ("federation", "iframe"):
        raise ApplicationError("INVALID_TYPE")
    data["frontend_url"] = _subApplicationNormalizeUrl(data["frontend_url"])
    data["backend_url"] = _subApplicationNormalizeUrl(data["backend_url"], optional=True)
    data["icon_url"] = _subApplicationNormalizeUrl(data["icon_url"], optional=True, icon=True)
    if data["app_type"] == "federation":
        if (
            data["remote_name"] == "cdi_pedestal"
            or not isinstance(data["remote_name"], str)
            or not re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_-]{0,63}", data["remote_name"])
        ):
            raise ApplicationError("INVALID_REMOTE")
        if (
            not isinstance(data["exposed_module"], str)
            or len(data["exposed_module"]) > 128
            or not re.fullmatch(
                r"\./[a-zA-Z0-9_-]+(?:/[a-zA-Z0-9_-]+)*", data["exposed_module"]
            )
        ):
            raise ApplicationError("INVALID_REMOTE")
    else:
        data.update(remote_name="", exposed_module="", backend_url="")
    for key in ("enabled", "show_in_menu", "require_login"):
        if type(data[key]) is not bool:
            raise ApplicationError("INVALID_FIELDS")
    if type(data["sort_order"]) is not int or not 0 <= data["sort_order"] <= 1000000:
        raise ApplicationError("INVALID_ORDER")
    return data


def _subApplicationListItem(
    row: SubApplication, authenticated: bool = False
) -> dict:
    """生成当前身份可见的子应用入口及后端直连地址。
    如果用户未登录且子应用需要登录，不返回敏感信息。
    """
    data = row.toJson()
    data["id"] = row.id
    data["api_base"] = row.backend_url
    data["has_backend"] = bool(row.backend_url)
    if row.require_login and not authenticated:
        data.update(frontend_url="", remote_name="", exposed_module="", backend_url="", api_base="")
    return data


def _subApplicationGetById(db: Session, app_id: int) -> SubApplication:
    """按 ID 获取未删除的子应用配置。"""
    row = db.get(SubApplication, app_id)
    if row is None or row.deleted_at is not None:
        raise ApplicationError("NOT_FOUND", 404)
    return row


def _subApplicationCheckAvailable(
    db: Session, data: dict, current_id: int | None = None
) -> None:
    """检查应用标识、路由和远程容器是否冲突。"""
    for row in db.query(SubApplication).with_for_update().all():
        if row.id == current_id:
            continue
        if row.app_key == data["app_key"] or row.route_path == data["route_path"]:
            raise ApplicationError("DUPLICATE_APPLICATION", 409)
        if row.deleted_at is None and (
            row.route_path.startswith(data["route_path"] + "/")
            or data["route_path"].startswith(row.route_path + "/")
        ):
            raise ApplicationError("ROUTE_CONFLICT", 409)
        if (
            row.deleted_at is None
            and data["app_type"] == "federation"
            and row.app_type == "federation"
            and {row.remote_name, row.app_key} & {data["remote_name"], data["app_key"]}
        ):
            raise ApplicationError("DUPLICATE_REMOTE", 409)


def subApplicationCreate(db: Session, values: dict, user_id: int) -> dict:
    """检查管理权限并创建子应用配置。"""
    _subApplicationRequireAuth(db=db, user_id=user_id)
    data = _subApplicationValidate(values)
    _subApplicationCheckAvailable(db=db, data=data)
    application = SubApplication(**data, created_by=user_id, updated_by=user_id)
    db.add(application)
    db.commit()
    db.refresh(application)
    return {
        "status": 201,
        "message": "Create sub application success",
        "item": application.toJson(),
    }


def subApplicationUpdate(
    db: Session, app_id: int, values: dict, user_id: int
) -> dict:
    """检查管理权限并更新子应用配置。"""
    _subApplicationRequireAuth(db=db, user_id=user_id)
    application = _subApplicationGetById(db=db, app_id=app_id)
    if not isinstance(values, dict):
        raise ApplicationError("INVALID_FIELDS")
    if "app_key" in values and values["app_key"] != application.app_key:
        raise ApplicationError("IMMUTABLE_KEY")
    data = _subApplicationValidate({
        **{key: getattr(application, key) for key in FIELDS},
        **values,
    })
    _subApplicationCheckAvailable(db=db, data=data, current_id=application.id)
    for key, value in data.items():
        setattr(application, key, value)
    application.updated_by = user_id
    application.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(application)
    return {
        "status": 200,
        "message": "Update sub application success",
        "item": application.toJson(),
    }


def subApplicationDelete(db: Session, app_id: int, user_id: int) -> dict:
    """检查管理权限并软删除子应用配置。"""
    _subApplicationRequireAuth(db=db, user_id=user_id)
    application = _subApplicationGetById(db=db, app_id=app_id)
    application.deleted_at = datetime.now(timezone.utc)
    application.updated_at = application.deleted_at
    application.enabled = False
    application.updated_by = user_id
    db.commit()
    return {"status": 200, "message": "Delete sub application success"}


def subApplicationReorder(db: Session, ids: list[int], user_id: int) -> dict:
    """检查管理权限并按完整 ID 列表更新排序。"""
    _subApplicationRequireAuth(db=db, user_id=user_id)
    if (
        not isinstance(ids, list)
        or any(type(app_id) is not int for app_id in ids)
        or len(set(ids)) != len(ids)
    ):
        raise ApplicationError("INVALID_ORDER")
    applications = (
        db.query(SubApplication)
        .filter(SubApplication.deleted_at.is_(None))
        .with_for_update()
        .all()
    )
    if set(ids) != {application.id for application in applications}:
        raise ApplicationError("INVALID_ORDER")
    by_id = {application.id: application for application in applications}
    for order, app_id in enumerate(ids):
        application = by_id[app_id]
        application.sort_order = order
        application.updated_by = user_id
        application.updated_at = datetime.now(timezone.utc)
    db.commit()
    return {"status": 200, "message": "Reorder sub applications success"}


def subApplicationGetList(
    db: Session,
    user_id: int | None = None,
    page: int = 1,
    page_size: int = 20,
    search: str = "",
    app_type: str = "",
    enabled: str = "",
) -> dict:
    """分页查询子应用列表并按登录状态隐藏受保护的入口。"""
    if user_id is not None and db.get(User, user_id) is None:
        raise ApplicationError("UNAUTHORIZED", 401)
    if page < 1 or not 1 <= page_size <= 100:
        raise ApplicationError("INVALID_PAGE")
    query = db.query(SubApplication).filter(SubApplication.deleted_at.is_(None))
    if search:
        query = query.filter(or_(
            SubApplication.app_key.contains(search, autoescape=True),
            SubApplication.name_zh.contains(search, autoescape=True),
            SubApplication.name_en.contains(search, autoescape=True),
        ))
    if app_type:
        if app_type not in ("federation", "iframe"):
            raise ApplicationError("INVALID_TYPE")
        query = query.filter(SubApplication.app_type == app_type)
    if enabled:
        if enabled not in ("true", "false"):
            raise ApplicationError("INVALID_FIELDS")
        query = query.filter(SubApplication.enabled == (enabled == "true"))
    total = query.count()
    applications = (
        query.order_by(SubApplication.sort_order, SubApplication.id)
        .limit(page_size)
        .offset((page - 1) * page_size)
        .all()
    )
    return {
        "status": 200,
        "message": "Get sub applications success",
        "items": [
            _subApplicationListItem(application, authenticated=user_id is not None)
            for application in applications
        ],
        "total": total,
    }


def subApplicationGetDetail(db: Session, app_id: int, user_id: int) -> dict:
    """检查管理权限并获取子应用完整配置。"""
    _subApplicationRequireAuth(db=db, user_id=user_id)
    application = _subApplicationGetById(db=db, app_id=app_id)
    return {
        "status": 200,
        "message": "Get sub application success",
        "item": application.toJson(),
    }
