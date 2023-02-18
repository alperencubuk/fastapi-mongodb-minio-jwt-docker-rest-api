from os import fstat, getenv, path, remove

from fastapi import Form, UploadFile


def remove_file(filename: str, user_id: str) -> None:
    file_path = f"{getenv('TEMP_FOLDER')}/{user_id}/{filename}"
    if path.exists(file_path):
        remove(file_path)


def file_size(file: UploadFile) -> int:
    return fstat(file.file.fileno()).st_size


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls
