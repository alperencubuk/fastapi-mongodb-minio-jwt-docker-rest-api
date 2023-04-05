from source.app.users.schemas import (
    UserCreate,
    UserRequest,
    UserUpdate,
    UserUpdateRequest,
)
from source.app.users.utils import check_email
from source.core.database import PyObjectId, db


async def create_user(user: UserRequest) -> dict | None:
    if await check_email(email=user.email):
        user = UserCreate(**user.dict())
        new_user = await db["user"].insert_one(user.dict())
        return await db["user"].find_one({"_id": new_user.inserted_id})


async def update_user(user_id: PyObjectId, user: UserUpdateRequest) -> dict | None:
    if not user.email or await check_email(email=user.email, user_id=user_id):
        user = UserUpdate(**user.dict())
        fields_to_update = {k: v for k, v in user.dict().items() if v is not None}
        await db["user"].update_one({"_id": user_id}, {"$set": fields_to_update})
        return await db["user"].find_one({"_id": user_id})


async def delete_user(user_id: PyObjectId) -> None:
    await db["user"].delete_one({"_id": user_id})


async def background_delete_user(user_id: PyObjectId) -> None:
    await db["storage"].delete_many({"user_id": user_id})
