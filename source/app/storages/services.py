from bson import ObjectId

from source.app.storages.schemas import (
    Storage,
    StorageCreate,
    StorageUpdate,
    StorageUpdateBase,
)
from source.app.storages.utils import check_storage, storage_exist
from source.core.database import db


async def create_storage(user_id: ObjectId, storage: Storage) -> dict:
    if not await check_storage(user_id=user_id, storage=storage):
        storage = StorageCreate(user_id=str(user_id), **storage.dict())
        new_storage = await db["storage"].insert_one(storage.dict())
        created_storage = await db["storage"].find_one({"_id": new_storage.inserted_id})
        return created_storage


async def update_storage(
    user_id: ObjectId, storage_id: ObjectId, storage: StorageUpdate
) -> dict:
    if await storage_exist(user_id=user_id, storage_id=storage_id):
        storage = StorageUpdateBase(**storage.dict())
        fields_to_update = {k: v for k, v in storage.dict().items() if v is not None}
        await db["storage"].update_one(
            {"_id": storage_id, "user_id": str(user_id)},
            {"$set": fields_to_update},
        )
        updated_storage = await db["storage"].find_one({"_id": storage_id})
        return updated_storage


async def get_storage(user_id: ObjectId, storage_id: ObjectId) -> dict:
    if storage := await db["storage"].find_one(
        {"_id": storage_id, "user_id": str(user_id)}
    ):
        return storage


async def get_all_storages(user_id: ObjectId) -> list:
    if (
        storages := await db["storage"]
        .find({"user_id": str(user_id)})
        .sort("updated_at", -1)
        .to_list(None)
    ):
        return storages
