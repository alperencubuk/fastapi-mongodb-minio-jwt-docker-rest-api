from fastapi import UploadFile
from pydantic import BaseModel

from source.app.files.utils import form_body


class FileDownload(BaseModel):
    storage_id: str
    file_path: str


@form_body
class FileUpload(BaseModel):
    file: UploadFile
    storage_id: str


class FileUploadResponse(BaseModel):
    filename: str
    storage_id: str
