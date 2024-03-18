import uuid

from fastapi import UploadFile, HTTPException, status, Depends
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye import Worker
from lonely_eye.auth.schemas import TokensInfo, AccessToken, RefreshToken
from lonely_eye.config import settings
from lonely_eye.database import database
from lonely_eye.workers.schemas import (
    WorkerRegistrationIn,
    WorkerRegistrationOut,
    WorkerJWT,
)
from lonely_eye.auth import utils as auth_utils
from lonely_eye.file_storage import service as file_storage_service
from lonely_eye.cache_memory import Keys as cache_memory_Keys, Keys


async def create_worker(
    photo: UploadFile,
    worker_in: WorkerRegistrationIn,
    session: AsyncSession,
):
    worker = await session.scalar(
        select(Worker).where(
            (Worker.username == worker_in.username)
            and (Worker.email == worker_in.email)
        )
    )
    if worker:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Worker already exists",
        )

    worker_in.password = auth_utils.hash_password(worker_in.password)
    worker = Worker(**worker_in.model_dump())

    session.add(worker)
    await session.commit()

    if not file_storage_service.upload_photo(
        file=photo.file,
        file_name=f"{worker.photo_id}.{settings.storage.photo_format}",
        bucket_name=settings.storage.worker_photo_storage_name,
    ):
        #  TODO: Save photo local
        pass

    return WorkerRegistrationOut(**worker_in.dict())


async def worker_login(
    worker: Worker,
    client: Redis,
) -> TokensInfo:

    refresh_token_id = str(uuid.uuid4())

    saved: bool = await client.set(
        name=cache_memory_Keys.worker(
            worker_id=worker.id,
            worker_username=worker.username,
        ),
        value=refresh_token_id,
        ex=settings.redis.refresh_token_expire_seconds,
    )

    if not saved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please, try again later...",
        )

    return auth_utils.tokens_info(
        pydantic_schema=worker,
        refresh_token_id=refresh_token_id,
    )


async def worker_refresh(
    worker_jwt: WorkerJWT,
    client: Redis,
):
    refresh_token_id = str(uuid.uuid4())

    deleted = await client.delete(
        cache_memory_Keys.worker(
            worker_id=worker_jwt.id,
            worker_username=worker_jwt.username,
        )
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Refresh-Token invalid",
        )

    return auth_utils.tokens_info(
        pydantic_schema=worker_jwt,
        refresh_token_id=refresh_token_id,
    )


async def worker_logout(access_token: AccessToken, client: Redis):
    await client.delete(
        Keys.worker(
            worker_id=access_token.sub,
            worker_username=access_token.username,
        )
    )


async def get_worker(
    username: str, session: AsyncSession = Depends(database.session_dependency)
) -> Worker:
    worker: Worker = await session.scalar(
        select(Worker).where(Worker.username == username)
    )
    if worker:
        return worker
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
