from fastapi import HTTPException, status
from pydantic import BaseModel, root_validator

from source.app.storages.enums import StorageEndpoint, StoragePlatform
from source.core.schemas import CreateModel, ResponseModel, UpdateModel


class Storage(BaseModel):
    name: str | None
    platform: str
    access_key: str
    secret_key: str
    bucket_name: str

    @root_validator
    def platform_validator(cls, values) -> dict:
        if platform := values.get("platform"):
            if platform not in StoragePlatform.values():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Platform must be in '{str(StoragePlatform.values())}'",
                )
        return values


class Endpoint(BaseModel):
    endpoint: str = None

    @root_validator
    def endpoint_validator(cls, values) -> dict:
        if platform := values.get("platform"):
            if platform == StoragePlatform.MINIO.value:
                values["endpoint"] = StorageEndpoint.MINIO.value
            elif platform == StoragePlatform.GOOGLE.value:
                values["endpoint"] = StorageEndpoint.GOOGLE.value
            elif platform == StoragePlatform.AWS.value:
                values["endpoint"] = StorageEndpoint.AWS.value
        return values


class StorageCreate(CreateModel, Endpoint, Storage):
    user_id: str


class StorageResponse(ResponseModel):
    name: str | None
    platform: str
    bucket_name: str


class StorageUpdate(Storage):
    platform: str | None
    access_key: str | None
    secret_key: str | None
    bucket_name: str | None


class StorageUpdateBase(UpdateModel, Endpoint, StorageUpdate):
    pass
