from datetime import datetime
from os import getenv

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, Field, root_validator
from pytz import timezone

from source.app.auth.utils import get_password_hash
from source.app.users.enums import UserRole
from source.core.schemas import CreateModel, ResponseModel, UpdateModel


class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: str | None
    last_name: str | None


class UserCreate(CreateModel, User):
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
        tz = timezone(getenv("TIME_ZONE"))
        values["created_at"] = (
            values.get("created_at").astimezone(tz=tz).strftime("%m.%d.%Y %H:%M:%S")
        )
        values["updated_at"] = (
            values.get("updated_at").astimezone(tz=tz).strftime("%m.%d.%Y %H:%M:%S")
        )
        return values


class UserUpdate(User):
    username: str | None
    password: str | None
    email: EmailStr | None


class UserUpdateAdmin(UserUpdate):
    role: str | None
    active: bool | None

    @root_validator
    def role_validator(cls, values) -> dict:
        if role := values.get("role"):
            if role not in UserRole.values():
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Role must be in '{str(UserRole.values())}'",
                )
        return values


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
