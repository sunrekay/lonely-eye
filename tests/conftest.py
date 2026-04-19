import asyncio
from typing import AsyncGenerator
from unittest.mock import patch

import dotenv
import pytest
from httpx import AsyncClient
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from lonely_eye.config import settings
from lonely_eye.database import database
from lonely_eye.models import Base
from lonely_eye.main import app

DB_NAME_TEST = "lonely_eye_test"

_base_url = settings.db.url.replace(
    f"/{settings.db.url.rsplit('/', 1)[-1]}", "/postgres"
)
DATABASE_URL_BASE = _base_url
DATABASE_URL_TEST = settings.db.url.rsplit("/", 1)[0] + f"/{DB_NAME_TEST}"

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(
    engine_test,
    class_=AsyncSession,
    expire_on_commit=False,
)
Base.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[database.session_dependency] = override_get_async_session


async def create_test_database():
    """Создаёт тестовую БД если её нет."""
    engine_base = create_async_engine(
        DATABASE_URL_BASE,
        poolclass=NullPool,
        isolation_level="AUTOCOMMIT",
    )
    async with engine_base.connect() as conn:
        result = await conn.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME_TEST}'")
        )
        exists = result.scalar()
        if not exists:
            await conn.execute(text(f'CREATE DATABASE "{DB_NAME_TEST}"'))
    await engine_base.dispose()


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    await create_test_database()
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True, scope="session")
def mock_s3():
    """Мокаем S3: upload всегда OK, get_photo_url возвращает фейковый URL."""
    with patch(
        "lonely_eye.file_storage.service.upload_photo",
        return_value=True,
    ), patch(
        "lonely_eye.file_storage.service.get_photo_url",
        return_value="https://fake-s3.example.com/photo.jpg",
    ):
        yield


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test/api/v1") as ac:
        yield ac


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def redis(event_loop):
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=0,
        decode_responses=True,
    )
    yield redis
    await redis.aclose()
