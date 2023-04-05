from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.background import BackgroundTasks

from source.app.auth.auth import auth
from source.app.users.schemas import User, UserRequest, UserResponse, UserUpdateRequest
from source.app.users.services import (
    background_delete_user,
    create_user,
    delete_user,
    update_user,
)
from source.core.schemas import ExceptionModel

user_router = APIRouter(prefix="/users")
CurrentUser = Annotated[User, Depends(auth)]


@user_router.post(
    "/",
    response_model=UserResponse,
    response_model_by_alias=False,
    responses={
        status.HTTP_409_CONFLICT: {"model": ExceptionModel},
    },
    status_code=status.HTTP_201_CREATED,
    tags=["users"],
)
async def user_create(user: UserRequest):
    if created_user := await create_user(user=user):
        return created_user
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"User '{user.email}' already exists",
    )


@user_router.get(
    "/",
    response_model=UserResponse,
    response_model_by_alias=False,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel}},
    tags=["users"],
)
async def user_get_me(user: CurrentUser):
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
async def user_update_me(payload: UserUpdateRequest, user: CurrentUser):
    if updated_user := await update_user(user_id=user.id, user=payload):
        return updated_user
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"User '{payload.email}' already exists",
    )


@user_router.delete(
    "/",
    response_model_by_alias=False,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel}},
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["users"],
)
async def user_delete_me(background_tasks: BackgroundTasks, user: CurrentUser):
    await delete_user(user_id=user.id)
    background_tasks.add_task(background_delete_user, user_id=user.id)
