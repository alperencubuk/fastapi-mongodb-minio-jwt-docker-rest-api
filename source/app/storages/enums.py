from enum import Enum
from os import getenv


class StoragePlatform(Enum):
    MINIO = "minio"
    GOOGLE = "google"
    AWS = "aws"

    @classmethod
    def values(cls) -> list:
        return [platform.value for platform in StoragePlatform]


class StorageEndpoint(Enum):
    MINIO = getenv("MINIO_ENDPOINT")
    GOOGLE = "storage.googleapis.com"
    AWS = "s3.amazonaws.com"
