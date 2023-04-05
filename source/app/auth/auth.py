from fastapi import Depends, HTTPException, Request, status

from source.app.auth.services import auth_access
from source.app.users.enums import UserRole


async def auth_header(request: Request) -> str | None:
    if authorization := request.headers.get("Authorization"):
        scheme, _, token = authorization.partition(" ")
        if scheme and token and scheme.lower() == "bearer":
            return token
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Authorization Header",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def auth_base(token: str, roles: list) -> dict:
    if user := await auth_access(token=token, roles=roles):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def auth(token: str = Depends(auth_header)) -> dict:
    return await auth_base(
        token=token, roles=[UserRole.USER.value, UserRole.ADMIN.value]
    )


async def auth_admin(token: str = Depends(auth_header)) -> dict:
    return await auth_base(token=token, roles=[UserRole.ADMIN.value])
