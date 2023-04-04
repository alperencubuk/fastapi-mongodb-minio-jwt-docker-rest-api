from fastapi import APIRouter, Depends, HTTPException, status

from source.app.auth.auth import auth, auth_admin
from source.app.users.schemas import (
    Username,
    UserRequest,
    UserResponse,
    UserResponseAdmin,
    UserUpdate,
    UserUpdateAdmin,
)
from source.app.users.services import (
    check_username_user,
    create_user,
    get_user,
    update_user,
)
from source.core.schemas import ExceptionModel

user_router = APIRouter(prefix="/users")


@user_router.post(
    "/",
    response_model=UserResponse,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": ExceptionModel},
    },
    tags=["users"],
)
async def user_create(user: UserRequest):
    if created_user := await create_user(user=user):
        return created_user
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Username '{user.username}' already exists",
    )


@user_router.get(
    "/",
    response_model=UserResponse,
    response_model_by_alias=False,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel}},
    tags=["users"],
)
async def user_get_me(user: dict = Depends(auth)):
    return user


@user_router.patch(
    "/",
    response_model=UserResponse,
    response_model_by_alias=False,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel},
        status.HTTP_409_CONFLICT: {"model": ExceptionModel},
    },
    tags=["users"],
)
async def user_update_me(payload: UserUpdate, user: dict = Depends(auth)):
    if updated_user := await update_user(user_id=user.get("_id"), user=payload):
        return updated_user
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Username '{payload.username}' already exists",
    )


@user_router.get(
    "/{username}",
    response_model=UserResponseAdmin,
    response_model_by_alias=False,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionModel},
    },
    tags=["admin"],
)
async def user_get(username: str, _=Depends(auth_admin)):
    if user := await get_user(username=username):
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User '{username}' not found"
    )


@user_router.patch(
    "/{username}",
    response_model=UserResponseAdmin,
    response_model_by_alias=False,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionModel},
        status.HTTP_409_CONFLICT: {"model": ExceptionModel},
    },
    tags=["admin"],
)
async def user_update(username: str, payload: UserUpdateAdmin, _=Depends(auth_admin)):
    if user := await get_user(username=username):
        if updated_user := await update_user(user_id=user.get("_id"), user=payload):
            return updated_user
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{payload.username}' already exists",
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User '{username}' not found"
    )


@user_router.get(
    "/username/{username}",
    response_model=Username,
    tags=["users"],
)
async def user_check_username(username: str):
    return await check_username_user(username=username)
