from robyn import SubRouter
from robyn.robyn import Request, Response
from robyn.authentication import BearerGetter

from authentication import AuthHandler
from database.database import session
from services.user import userGetUserIdByAccessToken
from services.sub_application import (
    subApplicationCreate,
    subApplicationUpdate,
    subApplicationDelete,
    subApplicationReorder,
    subApplicationGetList,
    subApplicationGetDetail,
)


subApplicationRouterV1 = SubRouter(__file__, prefix="/v1/sub-application")


# 全局异常处理
@subApplicationRouterV1.exception
def handle_exception(error):
    """返回接口执行异常。"""
    return Response(status_code=500, description=f"error msg: {error}", headers={})


# 鉴权中间件
subApplicationRouterV1.configure_authentication(AuthHandler(token_getter=BearerGetter()))


@subApplicationRouterV1.get("/list")
def getAllSubApplications(request: Request):
    """分页查询子应用列表，支持匿名及普通用户访问。"""
    user_id = (
        userGetUserIdByAccessToken(request=request)
        if request.headers.get("Authorization")
        else None
    )
    page = request.query_params.get("page", "1")
    page_size = request.query_params.get("page_size", "20")
    search = request.query_params.get("search", "")
    app_type = request.query_params.get("app_type", "")
    enabled = request.query_params.get("enabled", "")
    with session() as db:
        res = subApplicationGetList(
            db=db,
            user_id=user_id,
            page=int(page),
            page_size=int(page_size),
            search=search,
            app_type=app_type,
            enabled=enabled,
        )
    return res


@subApplicationRouterV1.get("/detail", auth_required=True)
def getSubApplicationById(request: Request):
    """通过子应用 ID 获取完整配置。"""
    app_id = request.query_params.get("id", "0")
    user_id = userGetUserIdByAccessToken(request=request)
    with session() as db:
        res = subApplicationGetDetail(db=db, app_id=int(app_id), user_id=user_id)
    return res


@subApplicationRouterV1.post("/create", auth_required=True)
def createSubApplication(request: Request):
    """创建子应用配置。"""
    data = request.json()
    user_id = userGetUserIdByAccessToken(request=request)
    with session() as db:
        res = subApplicationCreate(db=db, values=data, user_id=user_id)
    return res


@subApplicationRouterV1.post("/update", auth_required=True)
def updateSubApplication(request: Request):
    """修改子应用配置。"""
    data = request.json()
    user_id = userGetUserIdByAccessToken(request=request)
    with session() as db:
        res = subApplicationUpdate(
            db=db, app_id=int(data["id"]), values=data["values"], user_id=user_id
        )
    return res


@subApplicationRouterV1.post("/set-enabled", auth_required=True)
def setSubApplicationEnabled(request: Request):
    """启用或停用子应用。"""
    data = request.json()
    user_id = userGetUserIdByAccessToken(request=request)
    with session() as db:
        res = subApplicationUpdate(
            db=db,
            app_id=int(data["id"]),
            values={"enabled": data["enabled"]},
            user_id=user_id,
        )
    return res


@subApplicationRouterV1.post("/delete", auth_required=True)
def deleteSubApplicationById(request: Request):
    """软删除子应用。"""
    data = request.json()
    user_id = userGetUserIdByAccessToken(request=request)
    with session() as db:
        res = subApplicationDelete(db=db, app_id=int(data["id"]), user_id=user_id)
    return res


@subApplicationRouterV1.post("/reorder", auth_required=True)
def reorderSubApplications(request: Request):
    """更新全部子应用的排序。"""
    data = request.json()
    user_id = userGetUserIdByAccessToken(request=request)
    with session() as db:
        res = subApplicationReorder(db=db, ids=data["ids"], user_id=user_id)
    return res
