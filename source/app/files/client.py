from fastapi import HTTPException, UploadFile, status
from minio import Minio

from source.app.files.utils import file_size
from source.core.settings import settings


class MinioClient:
    def __init__(
        self, endpoint: str, access_key: str, secret_key: str, bucket_name: str
    ):
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=settings.MINIO_SECURE,
        )
        self.bucket_name = bucket_name

    def create_bucket(self):
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def upload_file(self, file: UploadFile):
        try:
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=file.filename,
                data=file.file,
                length=file_size(file),
            )
        except Exception as e:
            self._exception(f"Error while trying to upload file. Exception: {e}")

    def download_file(self, source: str, destination: str):
        try:
            self.client.fget_object(self.bucket_name, source, destination)
        except Exception as e:
            self._exception(f"Error while trying to download file. Exception: {e}")

    def _exception(self, detail: str):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )
