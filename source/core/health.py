from fastapi import status
from pymongo.errors import ConnectionFailure
from requests import get
from requests.exceptions import ConnectionError

from source.core.database import client
from source.core.settings import settings


async def mongodb_health() -> bool:
    try:
        await client.admin.command("ping")
        return True
    except ConnectionFailure:
        return False


async def minio_health() -> bool:
    try:
        if (
            get(url=f"http://{settings.MINIO_URI}/minio/health/live").status_code
            == status.HTTP_200_OK
        ):
            return True
        return False
    except ConnectionError:
        return False
