from asyncio import gather
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk import init

from source.app.users.utils import create_admin_user
from source.core.database import create_index
from source.core.health import database_health, storage_health
from source.core.routers import api_router
from source.core.schemas import HealthModel
from source.core.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await gather(create_index(), create_admin_user())
    yield


init(dsn=settings.SENTRY_DSN)

app = FastAPI(title=settings.APP_TITLE, version=settings.VERSION, lifespan=lifespan)

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
    database, storage = await gather(database_health(), storage_health())
    return {"api": True, "database": database, "storage": storage}
