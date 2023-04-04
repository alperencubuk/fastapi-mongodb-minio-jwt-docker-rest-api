from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, root_validator
from pytz import timezone

from source.app.auth.utils import get_password_hash
from source.app.users.enums import UserRole
from source.core.schemas import CreateModel, ResponseModel, UpdateModel
from source.core.settings import settings


class UserRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: str | None
    last_name: str | None


class User(CreateModel, UserRequest):
    role: str = UserRole.USER.value
    active: bool = True
    password_ts: float = Field(default_factory=datetime.utcnow().timestamp)

    @root_validator
    def password_validator(cls, values) -> dict:
        if password := values.get("password"):
            values["password"] = get_password_hash(password)
        return values


class UserResponse(ResponseModel):
    username: str
    email: EmailStr
    first_name: str | None
    last_name: str | None
    role: str


class UserResponseAdmin(UserResponse):
    active: bool = True
    created_at: datetime
    updated_at: datetime

    @root_validator
    def timezone_validator(cls, values) -> dict:
        tz = timezone(settings.TIME_ZONE)
        values["created_at"] = (
            values.get("created_at").astimezone(tz=tz).strftime("%m.%d.%Y %H:%M:%S")
        )
        values["updated_at"] = (
            values.get("updated_at").astimezone(tz=tz).strftime("%m.%d.%Y %H:%M:%S")
        )
        return values


class UserUpdate(UserRequest):
    username: str | None
    password: str | None
    email: EmailStr | None


class UserUpdateAdmin(UserUpdate):
    role: UserRole | None
    active: bool | None


class UserUpdateBase(UpdateModel, UserUpdateAdmin):
    password_ts: float | None

    @root_validator
    def password_validator(cls, values) -> dict:
        if password := values.get("password"):
            values["password"] = get_password_hash(password)
            values["password_ts"] = datetime.utcnow().timestamp()
        return values


class Username(BaseModel):
    username: str
    available: bool
