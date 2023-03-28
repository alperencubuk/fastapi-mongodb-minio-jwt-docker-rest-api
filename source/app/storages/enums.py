from enum import Enum
from os import getenv


class StoragePlatform(str, Enum):
    MINIO = "minio"
    GOOGLE = "google"
    AWS = "aws"


class StorageEndpoint(str, Enum):
    MINIO = getenv("MINIO_ENDPOINT")
    GOOGLE = "storage.googleapis.com"
    AWS = "s3.amazonaws.com"
