from datetime import datetime, timedelta

from fastapi import HTTPException, status
from jose import ExpiredSignatureError, JWTError, jwt
from jose.exceptions import JWTClaimsError

from source.app.auth.enums import TokenType
from source.app.auth.utils import verify_password
from source.core.database import PyObjectId, db
from source.core.settings import settings


async def authenticate_user(username: str, password: str) -> dict | None:
    if user := await db["user"].find_one({"username": username}):
        if verify_password(password, user.get("password")):
            if user.get("active"):
                return user
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your account is banned",
            )


async def authenticate_token(user_id: str, password_ts: float) -> dict | None:
    try:
        user_id = PyObjectId(user_id)
    except ValueError:
        return None
    if user := await db["user"].find_one({"_id": user_id}):
        if password_ts == user.get("password_ts"):
            if user.get("active"):
                return user
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Your account is banned",
            )


async def generate_token(user_id: PyObjectId, password_ts: float) -> dict:
    access = {
        "user_id": str(user_id),
        "password_ts": password_ts,
        "exp": datetime.utcnow()
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "type": TokenType.ACCESS.value,
    }
    refresh = access.copy()
    refresh.update(
        {
            "exp": datetime.utcnow()
            + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
            "type": TokenType.REFRESH.value,
        }
    )
    access_token = jwt.encode(access, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    refresh_token = jwt.encode(
        refresh, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


async def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except (JWTError, ExpiredSignatureError, JWTClaimsError):
        return None


async def auth_access(token: str, roles: list) -> dict | None:
    if payload := await decode_token(token):
        if payload.get("type") == TokenType.ACCESS.value:
            if user := await authenticate_token(
                payload.get("user_id"), payload.get("password_ts")
            ):
                if user.get("role") in roles:
                    return user


async def auth_refresh(token: str) -> dict | None:
    if payload := await decode_token(token):
        if payload.get("type") == TokenType.REFRESH.value:
            if user := await authenticate_token(
                payload.get("user_id"), payload.get("password_ts")
            ):
                return await generate_token(
                    user_id=user.get("_id"),
                    password_ts=user.get("password_ts"),
                )
