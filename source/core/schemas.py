from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field, root_validator

from source.core.database import PyObjectId


class CreateModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = None

    @root_validator
    def updated_at_validator(cls, values) -> dict:
        values["updated_at"] = values["created_at"]
        return values


class UpdateModel(BaseModel):
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ResponseModel(BaseModel):
    id: PyObjectId = Field(alias="_id")

    class Config:
        json_encoders = {ObjectId: str}


class ExceptionModel(BaseModel):
    detail: str


class HealthModel(BaseModel):
    api: bool
    mongodb: bool
    minio: bool
