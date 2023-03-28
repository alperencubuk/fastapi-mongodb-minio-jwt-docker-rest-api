from os import getenv

from source.app.files.client import MinioClient
from source.app.storages.schemas import Storage, StorageCreate
from source.app.users.services import get_user
from source.core.database import db, PyObjectId


async def check_storage(user_id: PyObjectId, storage: Storage) -> dict | None:
    if storage := await db["storage"].find_one(
        {"user_id": user_id, **storage.dict()}
    ):
        return storage


async def storage_exist(user_id: PyObjectId, storage_id: PyObjectId) -> dict | None:
    if storage := await db["storage"].find_one(
        {"_id": storage_id, "user_id": user_id}
    ):
        return storage


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
        storage = StorageCreate(user_id=user_id, **storage.dict())
        await db["storage"].insert_one(storage.dict())
        MinioClient(
            **storage.dict(
                include={"endpoint", "access_key", "secret_key", "bucket_name"}
            )
        ).create_bucket()
