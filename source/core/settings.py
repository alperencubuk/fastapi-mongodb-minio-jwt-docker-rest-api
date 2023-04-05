from functools import lru_cache

from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):
    APP_TITLE: str = "My Cloud"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin"
    ADMIN_EMAIL: str = "admin@admin.admin"
    TEMP_FOLDER: str = "temp"
    TIME_ZONE: str = "UTC"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    SECRET_KEY: str = "SECRET_KEY"
    ALGORITHM: str = "HS256"

    MONGO_INITDB_ROOT_USERNAME: str = "username"
    MONGO_INITDB_ROOT_PASSWORD: str = "password"
    MONGO_HOST: str = "mongodb"
    MONGO_PORT: int = 27017
    MONGO_URI: str = None

    MINIO_ROOT_USER: str = "username"
    MINIO_ROOT_PASSWORD: str = "password"
    MINIO_HOST: str = "minio"
    MINIO_PORT: int = 9000
    MINIO_SECURE: bool = False
    MINIO_BUCKET_NAME: str = "minio-bucket"
    MINIO_URI: str = None

    @root_validator
    def uri_validator(cls, values) -> dict:
        values["MONGO_URI"] = (
            f'mongodb://{values["MONGO_INITDB_ROOT_USERNAME"]}:{values["MONGO_INITDB_ROOT_PASSWORD"]}'
            f'@{values["MONGO_HOST"]}:{values["MONGO_PORT"]}'
        )
        values["MINIO_URI"] = f'{values["MINIO_HOST"]}:{values["MINIO_PORT"]}'
        return values


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
