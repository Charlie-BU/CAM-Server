from robyn.robyn import Request, Identity
from robyn.authentication import AuthenticationHandler

from database.database import session
from services.user import decodeAccessToken, userGetUserById

from database.enums import UserLevel


# 接口权限映射，value为访问该接口最低的用户等级
API_PERMISSION_MAP = {
    "/v1/user/getUserById": UserLevel.L0,
    "/v1/sub-application/create": UserLevel.L0,
    "/v1/sub-application/update": UserLevel.L0,
    "/v1/sub-application/set-enabled": UserLevel.L0,
    "/v1/sub-application/delete": UserLevel.L0,
    "/v1/sub-application/reorder": UserLevel.L0,
}


class AuthHandler(AuthenticationHandler):
    def authenticate(self, request: Request):
        token = self.token_getter.get_token(request)
        try:
            payload = decodeAccessToken(token or "")
            id = payload["id"]
        except Exception:
            return None
        with session() as db:
            user_response = userGetUserById(db, id)
            user = user_response.get("user")
            if user is None:
                return None
            # 检查接口权限
            api_path = request.url.path
            user_level = user["level"]
            if (
                api_path in API_PERMISSION_MAP
                and user_level.value > API_PERMISSION_MAP[api_path].value
            ):  # 在API_PERMISSION_MAP中，且用户等级低于最低要求，拒绝访问
                return None
        return Identity(claims={"user": f"{ user }"})
