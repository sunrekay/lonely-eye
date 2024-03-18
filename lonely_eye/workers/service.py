from fastapi import UploadFile, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye import Worker
from lonely_eye.config import settings
from lonely_eye.database import database
from lonely_eye.workers.schemas import (
    WorkerRegistrationIn,
    WorkerRegistrationOut,
)
from lonely_eye.auth import utils as auth_utils
from lonely_eye.auth import exceptions as auth_exceptions
from lonely_eye.file_storage import service as file_storage_service


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


async def get_worker(
    username: str, session: AsyncSession = Depends(database.session_dependency)
) -> Worker:
    worker: Worker = await session.scalar(
        select(Worker).where(Worker.username == username)
    )
    if worker:
        return worker
    raise auth_exceptions.wrong_login_password
