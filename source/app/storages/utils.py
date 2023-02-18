from os import getenv

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status

from source.app.files.client import MinioClient
from source.app.storages.schemas import Storage, StorageCreate
from source.app.users.services import get_user
from source.core.database import db


async def check_storage(user_id: ObjectId, storage: Storage) -> dict | None:
    if storage := await db["storage"].find_one(
        {"user_id": str(user_id), **storage.dict()}
    ):
        return storage


async def storage_exist(user_id: ObjectId, storage_id: ObjectId) -> dict | None:
    if storage := await db["storage"].find_one(
        {"_id": storage_id, "user_id": str(user_id)}
    ):
        return storage


async def set_storage_id(storage_id: str) -> ObjectId:
    try:
        return ObjectId(storage_id)
    except (InvalidId, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Storage id '{storage_id}' is not valid",
        )


async def create_minio_storage() -> None:
    admin_user = await get_user(username=getenv("ADMIN_USERNAME"))
    storage = Storage(
        name="admin_storage",
        platform="minio",
        access_key=getenv("MINIO_ROOT_USER"),
        secret_key=getenv("MINIO_ROOT_PASSWORD"),
        bucket_name=getenv("MINIO_BUCKET_NAME"),
    )
    user_id = admin_user.get("_id")
    if not await check_storage(user_id=user_id, storage=storage):
        storage = StorageCreate(user_id=str(user_id), **storage.dict())
        await db["storage"].insert_one(storage.dict())
        MinioClient(
            **storage.dict(
                include={"endpoint", "access_key", "secret_key", "bucket_name"}
            )
        ).create_bucket()
