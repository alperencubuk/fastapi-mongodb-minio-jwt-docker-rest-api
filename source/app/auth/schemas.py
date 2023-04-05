from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class Credentials(BaseModel):
    email: EmailStr
    password: str


class Refresh(BaseModel):
    refresh_token: str
