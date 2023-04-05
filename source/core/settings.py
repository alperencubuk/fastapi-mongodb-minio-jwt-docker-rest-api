from functools import lru_cache

from pydantic import BaseSettings, root_validator


class Settings(BaseSettings):
    APP_TITLE: str = "Chooch AI Vision Studio"
    VERSION: str = "1.0.0"

    ADMIN_EMAIL: str = "admin@chooch.com"
    ADMIN_PASSWORD: str = "ch0o_o0ch_@dm1n"

    SENTRY_DSN: str = ""

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    SECRET_KEY: str
    ALGORITHM: str = "HS256"

    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_HOST: str = "mongodb"
    MONGO_PORT: int = 27017
    MONGO_URI: str = None

    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_HOST: str = "minio"
    MINIO_PORT: int = 9000
    MINIO_SECURE: bool = False
    MINIO_BUCKET_NAME: str = "chooch-bucket"
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
