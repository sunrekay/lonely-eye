from typing import Type

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye.database import database
from lonely_eye.workers import service
from lonely_eye.workers.models import Worker
from lonely_eye.workers.schemas import WorkerLogin, WorkerJWT
from lonely_eye.auth import utils as auth_utils
from lonely_eye.auth import dependencies as auth_dependencies
from lonely_eye.auth import exceptions as auth_exceptions


http_bearer = HTTPBearer()


async def verify_login(
    worker_login: WorkerLogin,
    session: AsyncSession = Depends(database.session_dependency),
) -> Worker:
    worker: Worker = await service.get_worker(
        username=worker_login.username,
        session=session,
    )

    if not auth_utils.verify_password(
        password=worker_login.password,
        hashed_password=worker.password,
    ):
        raise auth_exceptions.wrong_login_password

    if worker.is_active:
        return worker

    raise auth_exceptions.worker_inactive


async def verify_refresh(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> WorkerJWT:

    token = credentials.credentials
    data = auth_dependencies.get_data_from_token(token)
    data["id"] = data.pop("sub")

    if data.get("token_id") is not None:
        return WorkerJWT(**data)

    raise auth_exceptions.wrong_token


async def verify_worker(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(database.session_dependency),
) -> Type[Worker] | None:

    access_token = credentials.credentials
    data = auth_dependencies.get_data_from_token(access_token)

    if "token_id" in data.keys():
        raise auth_exceptions.wrong_token

    try:
        worker_id = int(data["sub"])
    except (ValueError, TypeError):
        raise auth_exceptions.permission_denied

    worker = await session.get(Worker, worker_id)

    if worker is not None:
        return worker

    raise auth_exceptions.permission_denied
