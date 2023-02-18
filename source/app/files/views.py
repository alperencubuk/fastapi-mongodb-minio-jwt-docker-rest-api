from fastapi import APIRouter, Depends, status
from fastapi.background import BackgroundTasks
from fastapi.responses import FileResponse

from source.app.auth.auth import auth
from source.app.files.schemas import FileDownload, FileUpload, FileUploadResponse
from source.app.files.services import download_file, upload_file
from source.app.files.utils import remove_file
from source.core.schemas import ExceptionModel

file_router = APIRouter(prefix="/files", tags=["files"])


@file_router.post(
    "/",
    response_model=FileUploadResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionModel},
    },
    tags=["files"],
)
async def file_upload(file: FileUpload = Depends(), user: dict = Depends(auth)):
    if uploaded := await upload_file(
        user_id=user.get("_id"), storage_id=file.storage_id, file=file.file
    ):
        return uploaded


@file_router.get(
    "/",
    response_class=FileResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ExceptionModel},
        status.HTTP_404_NOT_FOUND: {"model": ExceptionModel},
    },
    tags=["files"],
)
async def file_download(
    background_tasks: BackgroundTasks,
    file: FileDownload = Depends(),
    user: dict = Depends(auth),
):
    background_tasks.add_task(
        remove_file, file.file_path.split("/")[-1], user.get("_id")
    )
    return await download_file(
        user_id=user.get("_id"), storage_id=file.storage_id, file_path=file.file_path
    )
