from asyncio import create_task
from contextlib import asynccontextmanager
from shutil import rmtree

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from source.app.storages.utils import create_minio_storage
from source.app.users.utils import create_admin_user
from source.core.settings import settings
from source.core.database import create_index
from source.core.health import minio_health, mongodb_health
from source.core.routers import api_router
from source.core.schemas import HealthModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_index()
    await create_admin_user()
    await create_minio_storage()
    yield
    rmtree(settings.TEMP_FOLDER, ignore_errors=True)


app = FastAPI(title=settings.APP_TITLE, lifespan=lifespan)

app.include_router(api_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthModel, tags=["health"])
async def health_check():
    mongodb_task = create_task(mongodb_health())
    minio_task = create_task(minio_health())
    mongodb = await mongodb_task
    minio = await minio_task
    return {"api": True, "mongodb": mongodb, "minio": minio}
