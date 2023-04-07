from source.app.users.schemas import User, UserRequest, UserUpdate, UserUpdateBase
from source.app.users.utils import check_username
from source.core.database import PyObjectId, db


async def check_username_user(username: str) -> dict:
    available = await check_username(username=username)
    return {"username": username, "available": available}


async def create_user(user: UserRequest) -> dict | None:
    if await check_username(username=user.username):
        user = User(**user.dict())
        new_user = await db["user"].insert_one(user.dict())
        created_user = await db["user"].find_one({"_id": new_user.inserted_id})
        return created_user


async def update_user(user_id: PyObjectId, user: UserUpdate) -> dict | None:
    if not user.username or await check_username(
        username=user.username, user_id=user_id
    ):
        user = UserUpdateBase(**user.dict())
        fields_to_update = {k: v for k, v in user.dict().items() if v is not None}
        return await db["user"].find_one_and_update(
            {"_id": user_id}, {"$set": fields_to_update}, return_document=True
        )


async def get_user(username: str) -> dict | None:
    if user := await db["user"].find_one({"username": username}):
        return user
