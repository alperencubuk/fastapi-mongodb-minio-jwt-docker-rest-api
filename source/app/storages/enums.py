from enum import Enum

from source.core.settings import settings


class StoragePlatform(str, Enum):
    MINIO = "minio"
    GOOGLE = "google"
    AWS = "aws"


class StorageEndpoint(str, Enum):
    MINIO = settings.MINIO_URI
    GOOGLE = "storage.googleapis.com"
    AWS = "s3.amazonaws.com"
