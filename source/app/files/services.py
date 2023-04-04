from fastapi import UploadFile

from source.app.files.client import MinioClient
from source.app.storages.services import get_storage
from source.core.database import PyObjectId
from source.core.settings import settings


async def upload_file(
    user_id: PyObjectId, storage_id: PyObjectId, file: UploadFile
) -> dict | None:
    if storage := await get_storage(user_id=user_id, storage_id=storage_id):
        client = MinioClient(
            endpoint=storage.get("endpoint"),
            access_key=storage.get("access_key"),
            secret_key=storage.get("secret_key"),
            bucket_name=storage.get("bucket_name"),
        )
        client.upload_file(file=file)
        return {"filename": file.filename, "storage_id": storage_id}


async def download_file(
    user_id: PyObjectId, storage_id: PyObjectId, file_path: str
) -> str | None:
    if storage := await get_storage(user_id=user_id, storage_id=storage_id):
        client = MinioClient(
            endpoint=storage.get("endpoint"),
            access_key=storage.get("access_key"),
            secret_key=storage.get("secret_key"),
            bucket_name=storage.get("bucket_name"),
        )
        destination_folder = f"{settings.TEMP_FOLDER}/{user_id}"
        filename = file_path.split("/")[-1]
        client.download_file(
            source=file_path, destination=f"{destination_folder}/{filename}"
        )
        return f"{destination_folder}/{filename}"
