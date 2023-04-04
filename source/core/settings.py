from functools import lru_cache

from pydantic import BaseSettings


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
    MONGODB_URI: str = f"mongodb://{MONGO_INITDB_ROOT_USERNAME}:{MONGO_INITDB_ROOT_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"

    MINIO_ROOT_USER: str = "username"
    MINIO_ROOT_PASSWORD: str = "password"
    MINIO_HOST: str = "minio"
    MINIO_PORT: int = 9000
    MINIO_SECURE: bool = False
    MINIO_BUCKET_NAME: str = "minio-bucket"
    MINIO_ENDPOINT: str = f"{MINIO_HOST}:{MINIO_PORT}"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
