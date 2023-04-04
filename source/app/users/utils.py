from source.app.users.enums import UserRole
from source.app.users.schemas import User, UserRequest
from source.core.database import PyObjectId, db
from source.core.settings import settings


async def check_username(username: str, user_id: PyObjectId = None) -> bool:
    if user := await db["user"].find_one({"username": username}):
        if user.get("_id") != user_id:
            return False
    return True


async def create_admin_user() -> None:
    if await check_username(username=settings.ADMIN_USERNAME):
        user = UserRequest(
            username=settings.ADMIN_USERNAME,
            password=settings.ADMIN_PASSWORD,
            email=settings.ADMIN_EMAIL,
        )
        user = User(**user.dict(), role=UserRole.ADMIN.value)
        await db["user"].insert_one(user.dict())
