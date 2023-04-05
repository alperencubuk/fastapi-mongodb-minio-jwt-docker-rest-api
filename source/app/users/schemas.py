from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, root_validator, validator

from source.app.auth.utils import get_password_hash
from source.app.users.enums import UserRole
from source.core.schemas import CreateModel, ResponseModel, UpdateModel


class UserRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None
    last_name: str | None


class UserCreate(CreateModel, UserRequest):
    role: str = UserRole.USER.value
    active: bool = True
    password_ts: float = Field(default_factory=datetime.utcnow().timestamp)

    @validator('password')
    def password_validator(cls, password) -> dict:
        password = get_password_hash(password)
        return password


class UserResponse(ResponseModel):
    email: EmailStr
    first_name: str | None
    last_name: str | None
    role: str


class UserUpdateRequest(UserRequest):
    email: EmailStr | None
    password: str | None


class UserUpdate(UpdateModel, UserUpdateRequest):
    password_ts: float | None

    @root_validator
    def password_validator(cls, values) -> dict:
        if password := values.get("password"):
            values["password"] = get_password_hash(password)
            values["password_ts"] = datetime.utcnow().timestamp()
        return values


class User(ResponseModel, UserCreate):
    pass
