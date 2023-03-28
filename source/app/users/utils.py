from os import getenv

from source.app.users.enums import UserRole
from source.app.users.schemas import User, UserCreate
from source.core.database import db, PyObjectId


async def check_username(username: str, user_id: PyObjectId = None) -> bool:
    if user := await db["user"].find_one({"username": username}):
        if user.get("_id") != user_id:
            return False
    return True


async def create_admin_user() -> None:
    if await check_username(username=getenv("ADMIN_USERNAME")):
        user = User(
            username=getenv("ADMIN_USERNAME"),
            password=getenv("ADMIN_PASSWORD"),
            email=getenv("ADMIN_EMAIL"),
        )
        user = UserCreate(**user.dict(), role=UserRole.ADMIN.value)
        await db["user"].insert_one(user.dict())
