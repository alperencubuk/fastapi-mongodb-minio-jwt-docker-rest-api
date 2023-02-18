from os import getenv

from fastapi import status
from pymongo.errors import ConnectionFailure
from requests import get
from requests.exceptions import ConnectionError

from source.core.database import client


async def mongodb_health() -> bool:
    try:
        await client.admin.command("ping")
        return True
    except ConnectionFailure:
        return False


async def minio_health() -> bool:
    try:
        if (
            get(url=f"http://{getenv('MINIO_ENDPOINT')}/minio/health/live").status_code
            == status.HTTP_200_OK
        ):
            return True
        return False
    except ConnectionError:
        return False
