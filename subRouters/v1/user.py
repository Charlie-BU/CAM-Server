import json

from services.user import (
    GoogleAuthError,
    userGetUserByUsernameOrNicknameOrEmail,
    userGoogleLogin,
    userLinkGoogleIdentity,
    userModifyPassword,
)
from robyn import SubRouter
from robyn.robyn import Request, Response
from robyn.authentication import BearerGetter

from authentication import AuthHandler
from database.database import session
from services.user import (
    userGetUserIdByAccessToken,
    userLogin,
    userListUsers,
    userRegister,
    userGetUserById,
)

userRouterV1 = SubRouter(__file__, prefix="/v1/user")


# 全局异常处理
@userRouterV1.exception
def handle_exception(error):
    return Response(status_code=500, description=f"error msg: {error}", headers={})


# 鉴权中间件
userRouterV1.configure_authentication(AuthHandler(token_getter=BearerGetter()))


def googleAuthErrorResponse(error: GoogleAuthError):
    return Response(
        status_code=error.http_status,
        description=json.dumps(
            {
                "status": error.http_status,
                "code": error.code,
                "message": error.message,
            }
        ),
        headers={"Content-Type": "application/json"},
    )


# 通过用户id获取用户详情
@userRouterV1.get("/getUserById", auth_required=True)
async def getUserById(request: Request):
    id = request.query_params.get("id", None)
    if not id:
        return Response(
            status_code=400,
            description="id is required",
            headers={},
        )
    with session() as db:
        res = userGetUserById(db=db, id=int(id))
    return res


# 通过access_token获取用户详情
@userRouterV1.get("/getMyInfo", auth_required=True)
async def getMyInfo(request: Request):
    user_id = userGetUserIdByAccessToken(request=request)
    with session() as db:
        res = userGetUserById(db=db, id=user_id)
    return res


# 通过用户名或昵称或邮箱获取用户信息
@userRouterV1.get("/getUserByUsernameOrNicknameOrEmail", auth_required=True)
async def getUserByUsernameOrNicknameOrEmail(request: Request):
    username_or_nickname_or_email = request.query_params.get(
        "username_or_nickname_or_email", None
    )
    if not username_or_nickname_or_email:
        return Response(
            status_code=400,
            description="username_or_nickname_or_email is required",
            headers={},
        )
    with session() as db:
        res = userGetUserByUsernameOrNicknameOrEmail(
            db=db,
            username_or_nickname_or_email=username_or_nickname_or_email,
        )
    return res


# 成员目录沿用登录认证，对所有 CDI 用户开放。
@userRouterV1.get("/listUsers", auth_required=True)
async def listUsers(request: Request):
    try:
        after_id = int(request.query_params.get("after_id", "0"))
        limit = int(request.query_params.get("limit", "100"))
        raw_user = request.query_params.get("user_id", None)
        user_id = int(raw_user) if raw_user is not None else None
        if not 0 <= after_id <= 9223372036854775807 or not 1 <= limit <= 100 or (user_id is not None and not 1 <= user_id <= 9223372036854775807):
            raise ValueError("Invalid user query")
    except (TypeError, ValueError):
        return Response(status_code=400, description=json.dumps({"status": 400, "message": "Invalid user query"}), headers={"Content-Type": "application/json"})
    with session() as db:
        return userListUsers(db, after_id, limit, user_id)


# 用户登录
@userRouterV1.post("/login")
async def login(request: Request):
    data = request.json()
    username = data["username"]
    password = data["password"]
    with session() as db:
        res = userLogin(db=db, username=username, password=password)
    return res


# Google 用户登录
@userRouterV1.post("/login/google")
async def googleLogin(request: Request):
    data = request.json()
    credential = data.get("credential", "") if isinstance(data, dict) else ""
    try:
        with session() as db:
            return userGoogleLogin(db=db, credential=credential)
    except GoogleAuthError as error:
        return googleAuthErrorResponse(error)


# 为当前用户绑定 Google 身份
@userRouterV1.post("/link/google", auth_required=True)
async def linkGoogle(request: Request):
    data = request.json()
    credential = data.get("credential", "") if isinstance(data, dict) else ""
    user_id = userGetUserIdByAccessToken(request=request)
    try:
        with session() as db:
            return userLinkGoogleIdentity(
                db=db,
                user_id=user_id,
                credential=credential,
            )
    except GoogleAuthError as error:
        return googleAuthErrorResponse(error)


# 用户注册
@userRouterV1.post("/register")
async def register(request: Request):
    data = request.json()
    username = data["username"]
    password = data["password"]
    nickname = data["nickname"]
    email = data["email"]
    role = data["role"]
    with session() as db:
        res = userRegister(
            db=db,
            username=username,
            password=password,
            nickname=nickname,
            email=email,
            role=role,
        )
    return res


# 修改密码
@userRouterV1.post("/modifyPassword", auth_required=True)
async def modifyPassword(request: Request):
    data = request.json()
    id = userGetUserIdByAccessToken(request=request)
    old_password = data.get("old_password", "")
    new_password = data["new_password"]
    with session() as db:
        res = userModifyPassword(
            db=db,
            id=id,
            old_password=old_password,
            new_password=new_password,
        )
    return res
