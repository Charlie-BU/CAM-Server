from urllib.parse import unquote
from robyn.robyn import Request
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from jose import jwt
from google.auth.exceptions import TransportError
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
import hashlib
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

from database.models import User, UserAuthIdentity
from database.enums import UserRole

# 加载 .env 文件
load_dotenv()
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("LOGIN_SECRET")


class GoogleAuthError(Exception):
    def __init__(self, http_status: int, code: str, message: str):
        super().__init__(message)
        self.http_status = http_status
        self.code = code
        self.message = message


# 生成access token
def createAccessToken(
    data: dict, expires_delta: timedelta | None = timedelta(hours=24)
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    if not ALGORITHM or not SECRET_KEY:
        raise Exception("ALGORITHM or SECRET_KEY is not set in .env file")
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# 解析access token
def decodeAccessToken(token: str) -> dict:
    if not ALGORITHM or not SECRET_KEY:
        raise Exception("ALGORITHM or SECRET_KEY is not set in .env file")
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


# 通过access token获取user id
def userGetUserIdByAccessToken(
    request: Request | None = None, token: str | None = None
) -> int:
    if request is not None and token is not None:
        raise Exception("Request and token should not be provided at the same time")
    if request is not None:
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise Exception("Invalid Authorization header format")
        token = authorization.split("Bearer ")[1]
    elif token is None:
        raise Exception("Either request or token is required")
    payload = decodeAccessToken(token)
    return payload["id"]


# 通过user id获取user信息
def userGetUserById(db: Session, id: int) -> dict:
    user = db.get(User, id)
    if user is None:
        return {
            "status": -1,
            "message": "User not found",
        }
    return {
        "status": 200,
        "message": "Get user success",
        "user": user.toJson(),
    }


def _googleAllowedDomains() -> set[str] | None:
    """读取 Google 登录组织白名单。"""
    raw = os.getenv("GOOGLE_ORG_ALLOW_LIST")
    if raw is None:
        return None
    try:
        domains = json.loads(raw)
        if not isinstance(domains, list) or any(
            not isinstance(domain, str) or not domain.strip()
            for domain in domains
        ):
            raise ValueError("Expected a JSON array of nonempty domains")
    except ValueError as error:
        raise GoogleAuthError(
            503,
            "GOOGLE_AUTH_NOT_CONFIGURED",
            "Google organization allow list is invalid",
        ) from error
    return {domain.strip().lower() for domain in domains}


def verifyGoogleCredential(credential: str) -> dict:
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    if not client_id:
        raise GoogleAuthError(
            503,
            "GOOGLE_AUTH_NOT_CONFIGURED",
            "Google login is not configured",
        )
    if not credential:
        raise GoogleAuthError(400, "INVALID_REQUEST", "credential is required")
    allowed_domains = _googleAllowedDomains()
    try:
        payload = google_id_token.verify_oauth2_token(
            credential,
            google_requests.Request(),
            client_id,
        )
    except ValueError as error:
        raise GoogleAuthError(
            401,
            "INVALID_GOOGLE_CREDENTIAL",
            "Invalid Google credential",
        ) from error
    except TransportError as error:
        raise GoogleAuthError(
            503,
            "GOOGLE_AUTH_UNAVAILABLE",
            "Google identity verification is temporarily unavailable",
        ) from error

    if payload.get("iss") not in {"accounts.google.com", "https://accounts.google.com"}:
        raise GoogleAuthError(
            401,
            "INVALID_GOOGLE_CREDENTIAL",
            "Invalid Google credential issuer",
        )
    subject = payload.get("sub")
    email = payload.get("email")
    if not subject or not email or payload.get("email_verified") is not True:
        raise GoogleAuthError(
            401,
            "UNVERIFIED_GOOGLE_ACCOUNT",
            "Google account email is not verified",
        )
    if len(str(subject)) > 255 or len(str(email).strip()) > 128:
        raise GoogleAuthError(
            401,
            "INVALID_GOOGLE_CREDENTIAL",
            "Google account identity is too long",
        )
    hosted_domain = str(payload.get("hd") or "").strip().lower()
    email_domain = str(email).strip().lower().rsplit("@", 1)
    if allowed_domains is not None and (
        hosted_domain not in allowed_domains
        or len(email_domain) != 2
        or email_domain[1] not in allowed_domains
    ):
        raise GoogleAuthError(
            403,
            "GOOGLE_DOMAIN_NOT_ALLOWED",
            "Google account domain is not allowed",
        )
    return payload


def _googleUsername(db: Session, subject: str) -> str:
    digest = hashlib.sha256(subject.encode("utf-8")).hexdigest()
    for length in range(24, 57, 8):
        username = f"google_{digest[:length]}"
        if db.query(User).filter(User.username == username).first() is None:
            return username
    raise GoogleAuthError(409, "USERNAME_CONFLICT", "Unable to allocate username")


def _issueUserAccessToken(user: User) -> dict:
    access_token = createAccessToken(data={"id": user.id, "username": user.username})
    return {
        "status": 200,
        "message": "Login success",
        "access_token": access_token,
    }


def userGoogleLogin(db: Session, credential: str) -> dict:
    payload = verifyGoogleCredential(credential)
    subject = str(payload["sub"])
    email = str(payload["email"]).strip().lower()
    identity = (
        db.query(UserAuthIdentity)
        .filter(
            UserAuthIdentity.provider == "google",
            UserAuthIdentity.provider_subject == subject,
        )
        .first()
    )
    if identity is not None:
        identity.provider_email = email
        identity.last_login_at = datetime.now(timezone.utc)
        db.commit()
        return _issueUserAccessToken(identity.user)

    existing_user = (
        db.query(User).filter(func.lower(User.email) == email).first()
    )
    if existing_user is not None:
        raise GoogleAuthError(
            409,
            "ACCOUNT_LINK_REQUIRED",
            "An account with this email already exists; sign in with your password to link Google",
        )

    user = User(
        username=_googleUsername(db, subject),
        password=None,
        nickname=(str(payload.get("name") or email).strip()[:64] or email[:64]),
        email=email,
        role=UserRole.GUEST,
    )
    identity = UserAuthIdentity(
        user=user,
        provider="google",
        provider_subject=subject,
        provider_email=email,
    )
    # SQLAlchemy 的 save-update 级联会在添加身份记录时一并将新用户加入 Session。
    db.add(identity)
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        concurrent_identity = (
            db.query(UserAuthIdentity)
            .filter(
                UserAuthIdentity.provider == "google",
                UserAuthIdentity.provider_subject == subject,
            )
            .first()
        )
        if concurrent_identity is None:
            raise GoogleAuthError(
                409,
                "ACCOUNT_CONFLICT",
                "Google account could not be created",
            ) from error
        return _issueUserAccessToken(concurrent_identity.user)
    db.refresh(user)
    return _issueUserAccessToken(user)


def userLinkGoogleIdentity(db: Session, user_id: int, credential: str) -> dict:
    payload = verifyGoogleCredential(credential)
    subject = str(payload["sub"])
    email = str(payload["email"]).strip().lower()
    user = db.get(User, user_id)
    if user is None:
        raise GoogleAuthError(404, "USER_NOT_FOUND", "User not found")
    if not user.email or user.email.strip().lower() != email:
        raise GoogleAuthError(
            409,
            "GOOGLE_EMAIL_MISMATCH",
            "Google account email must match the current account email",
        )

    existing_identity = (
        db.query(UserAuthIdentity)
        .filter(
            UserAuthIdentity.provider == "google",
            UserAuthIdentity.provider_subject == subject,
        )
        .first()
    )
    if existing_identity is not None:
        if existing_identity.user_id != user_id:
            raise GoogleAuthError(
                409,
                "GOOGLE_IDENTITY_ALREADY_LINKED",
                "Google account is already linked to another user",
            )
        return {"status": 200, "message": "Google account already linked"}

    user_identity = (
        db.query(UserAuthIdentity)
        .filter(
            UserAuthIdentity.user_id == user_id,
            UserAuthIdentity.provider == "google",
        )
        .first()
    )
    if user_identity is not None:
        raise GoogleAuthError(
            409,
            "GOOGLE_IDENTITY_ALREADY_LINKED",
            "Current user already has a linked Google account",
        )
    db.add(
        UserAuthIdentity(
            user_id=user_id,
            provider="google",
            provider_subject=subject,
            provider_email=email,
        )
    )
    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise GoogleAuthError(
            409,
            "GOOGLE_IDENTITY_ALREADY_LINKED",
            "Google account is already linked",
        ) from error
    return {"status": 200, "message": "Google account linked"}


# 通过用户名或昵称或邮箱获取用户信息
def userGetUserByUsernameOrNicknameOrEmail(
    db: Session, username_or_nickname_or_email: str
) -> dict:
    # 把 url 编码的字符串解码，否则是 %20 等格式
    keyword = unquote(username_or_nickname_or_email).strip()
    search_users = (
        db.query(User)
        .filter(
            or_(
                User.username.ilike(f"%{keyword}%"),
                User.nickname.ilike(f"%{keyword}%"),
                User.email.ilike(f"%{keyword}%"),
            )
        )
        .order_by(User.nickname, User.username, User.email)
        .all()
    )
    return {
        "status": 200,
        "message": "Get users success",
        "users": [user.toJson() for user in search_users] if search_users else [],
    }


# 用户登录
def userLogin(db: Session, username: str, password: str) -> dict:
    user = (
        db.query(User)
        .filter(or_(User.username == username, User.email == username))
        .first()
    )
    if user is None:
        return {
            "status": -1,
            "message": "User not found",
        }
    if not user.checkPassword(password):
        return {
            "status": -2,
            "message": "Wrong password",
        }
    access_token = createAccessToken(data={"id": user.id, "username": user.username})
    return {
        "status": 200,
        "message": "Login success",
        "access_token": access_token,
    }


# 用户注册
def userRegister(
    db: Session, username: str, password: str, nickname: str, email: str, role: str
) -> dict:
    existing_user = (
        db.query(User)
        .filter(or_(User.username == username, User.email == email))
        .first()
    )
    if existing_user:
        return {
            "status": -1,
            "message": "Username or email already registered",
        }
    try:
        user_role = UserRole(role)
    except ValueError:
        user_role = UserRole.GUEST
    user = User(
        username=username,
        password=User.hashPassword(password),
        nickname=nickname,
        email=email,
        role=user_role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "status": 200,
        "message": "Register success",
    }


# 修改密码
def userModifyPassword(
    db: Session, id: int, old_password: str, new_password: str
) -> dict:
    user = db.get(User, id)
    if user is None:
        return {
            "status": -1,
            "message": "User not found",
        }
    if not old_password or old_password.strip() == "":
        if user.password:
            return {
                "status": -2,
                "message": "Old password cannot be empty",
            }
        user.password = User.hashPassword(new_password)  # type: ignore
        db.commit()
        return {
            "status": 200,
            "message": "Set password success",
        }
    if not user.password:
        return {
            "status": -4,
            "message": "This account does not have a local password",
        }
    if not user.checkPassword(old_password):
        return {
            "status": -2,
            "message": "Wrong old password",
        }
    if old_password == new_password:
        return {
            "status": -3,
            "message": "New password cannot be the same as old password",
        }
    user.password = User.hashPassword(new_password)  # type: ignore
    db.commit()
    return {
        "status": 200,
        "message": "Modify password success",
    }
