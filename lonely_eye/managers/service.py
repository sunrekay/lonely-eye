from redis.asyncio import Redis
from sqlalchemy import select, update, Result
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye import Manager, Worker
from lonely_eye.config import settings
from lonely_eye.managers import exceptions
from lonely_eye.managers.schemas import ManagerLogin, ActivateWorkerOut, WorkerOut
from lonely_eye.auth import exceptions as auth_exceptions
from lonely_eye.file_storage import service as file_storage_service
from lonely_eye.cache_memory import Keys as key_generator


async def get_manager(
    manager_login: ManagerLogin,
    session: AsyncSession,
) -> Manager:
    stmt = select(Manager).where(Manager.username == manager_login.username)
    manager = await session.scalar(stmt)
    if manager:
        return manager
    raise auth_exceptions.wrong_login_password


async def activate_worker(
    username: str,
    manager: Manager,
    session: AsyncSession,
):
    stmt = update(Worker).values(is_active=True).where(Worker.username == username)
    res = await session.execute(stmt)
    await session.commit()
    if res.rowcount:
        return ActivateWorkerOut()
    raise exceptions.activate_worker_username_wrong


async def get_workers(client: Redis, session: AsyncSession) -> list[WorkerOut]:
    stmt = select(Worker).order_by(Worker.id)
    result: Result = await session.execute(stmt)
    workers = result.scalars().all()

    l: list = []
    for worker in list(workers):
        worker_out: WorkerOut = WorkerOut(**worker.__dict__)

        url = await client.get(
            name=key_generator.worker_photo_url(
                worker.id,
                worker.username,
            )
        )
        if url is not None:
            worker_out.photo_url = url

        else:
            url = file_storage_service.get_photo_url(
                bucket_name=settings.storage.worker_photo_storage_name,
                file_name=f"{worker.photo_id}.{settings.storage.photo_format}",
            )
            worker_out.photo_url = url
            await client.set(
                name=key_generator.worker_photo_url(
                    worker.id,
                    worker.username,
                ),
                value=url,
            )

        l.append(worker_out)

    return l
