from bson import ObjectId
from fastapi import UploadFile
from pydantic import BaseModel

from source.app.files.utils import form_body
from source.core.database import PyObjectId


class FileDownload(BaseModel):
    storage_id: PyObjectId
    file_path: str


@form_body
class FileUpload(BaseModel):
    file: UploadFile
    storage_id: PyObjectId


class FileUploadResponse(BaseModel):
    filename: str
    storage_id: PyObjectId

    class Config:
        json_encoders = {ObjectId: str}
