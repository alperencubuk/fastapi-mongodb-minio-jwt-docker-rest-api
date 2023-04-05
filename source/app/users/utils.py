from pydantic import EmailStr

from source.app.users.enums import UserRole
from source.app.users.schemas import UserCreate
from source.core.database import PyObjectId, db
from source.core.settings import settings


async def check_email(email: EmailStr, user_id: PyObjectId = None) -> bool:
    if user := await db["user"].find_one({"email": email}):
        if user.get("_id") != user_id:
            return False
    return True


async def create_admin_user() -> None:
    if await check_email(email=settings.ADMIN_EMAIL):
        user = UserCreate(
            email=settings.ADMIN_EMAIL,
            password=settings.ADMIN_PASSWORD,
            role=UserRole.ADMIN.value,
        )
        await db["user"].insert_one(user.dict())
