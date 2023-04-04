from pydantic import BaseModel, root_validator

from source.app.storages.enums import StorageEndpoint, StoragePlatform
from source.core.database import PyObjectId
from source.core.schemas import CreateModel, ResponseModel, UpdateModel


class StorageRequest(BaseModel):
    name: str | None
    platform: StoragePlatform
    access_key: str
    secret_key: str
    bucket_name: str


class Endpoint(BaseModel):
    endpoint: StorageEndpoint = None

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


class Storage(CreateModel, Endpoint, StorageRequest):
    user_id: PyObjectId


class StorageResponse(ResponseModel):
    name: str | None
    platform: StoragePlatform
    bucket_name: str


class StorageUpdate(StorageRequest):
    platform: StoragePlatform | None
    access_key: str | None
    secret_key: str | None
    bucket_name: str | None


class StorageUpdateBase(UpdateModel, Endpoint, StorageUpdate):
    pass


class StorageId(BaseModel):
    storage_id: PyObjectId
