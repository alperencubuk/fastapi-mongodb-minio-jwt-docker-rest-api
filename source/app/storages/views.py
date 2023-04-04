from fastapi import APIRouter, Depends, HTTPException, status

from source.app.auth.auth import auth
from source.app.storages.schemas import (
    StorageId,
    StorageRequest,
    StorageResponse,
    StorageUpdate,
)
from source.app.storages.services import (
    create_storage,
    get_all_storages,
    get_storage,
    update_storage,
)
from source.core.schemas import ExceptionModel

storage_router = APIRouter(prefix="/storages", tags=["storages"])


@storage_router.post(
    "/",
    response_model=StorageResponse,
    response_model_exclude_none=True,
    response_model_by_alias=False,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel},
        status.HTTP_409_CONFLICT: {"model": ExceptionModel},
    },
    tags=["storages"],
)
async def storage_create(storage: StorageRequest, user: dict = Depends(auth)):
    if created_storage := await create_storage(
        user_id=user.get("_id"), storage=storage
    ):
        return created_storage
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Storage already exists",
    )


@storage_router.get(
    "/",
    response_model=list[StorageResponse],
    response_model_exclude_none=True,
    response_model_by_alias=False,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel}},
    tags=["storages"],
)
async def storage_get_all(user: dict = Depends(auth)):
    return await get_all_storages(user_id=user.get("_id"))


@storage_router.get(
    "/{storage_id}",
    response_model=StorageResponse,
    response_model_exclude_none=True,
    response_model_by_alias=False,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionModel},
    },
    tags=["storages"],
)
async def storage_get(payload: StorageId = Depends(), user: dict = Depends(auth)):
    if storage := await get_storage(
        user_id=user.get("_id"), storage_id=payload.storage_id
    ):
        return storage
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Storage '{payload.storage_id}' not found",
    )


@storage_router.patch(
    "/{storage_id}",
    response_model=StorageResponse,
    response_model_exclude_none=True,
    response_model_by_alias=False,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionModel},
    },
    tags=["storages"],
)
async def storage_update(
    storage: StorageUpdate,
    payload: StorageId = Depends(),
    user: dict = Depends(auth),
):
    if updated_storage := await update_storage(
        user_id=user.get("_id"), storage_id=payload.storage_id, storage=storage
    ):
        return updated_storage
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Storage '{payload.storage_id}' not found",
    )
