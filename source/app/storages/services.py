from source.app.storages.schemas import (
    Storage,
    StorageRequest,
    StorageUpdate,
    StorageUpdateBase,
)
from source.app.storages.utils import check_storage, storage_exist
from source.core.database import PyObjectId, db


async def create_storage(user_id: PyObjectId, storage: StorageRequest) -> dict | None:
    if not await check_storage(user_id=user_id, storage=storage):
        storage = Storage(user_id=user_id, **storage.dict())
        new_storage = await db["storage"].insert_one(storage.dict())
        created_storage = await db["storage"].find_one({"_id": new_storage.inserted_id})
        return created_storage


async def update_storage(
    user_id: PyObjectId, storage_id: PyObjectId, storage: StorageUpdate
) -> dict | None:
    if await storage_exist(user_id=user_id, storage_id=storage_id):
        storage = StorageUpdateBase(**storage.dict())
        fields_to_update = {k: v for k, v in storage.dict().items() if v is not None}
        return await db["storage"].find_one_and_update(
            {"_id": storage_id, "user_id": user_id},
            {"$set": fields_to_update},
            return_document=True,
        )


async def get_storage(user_id: PyObjectId, storage_id: PyObjectId) -> dict | None:
    if storage := await db["storage"].find_one({"_id": storage_id, "user_id": user_id}):
        return storage


async def get_all_storages(user_id: PyObjectId) -> list:
    return (
        await db["storage"]
        .find({"user_id": user_id})
        .sort("updated_at", -1)
        .to_list(None)
    )
