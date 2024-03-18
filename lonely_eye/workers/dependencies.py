from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye.auth.schemas import AccessToken
from lonely_eye.database import database
from lonely_eye.workers import service
from lonely_eye.workers.models import Worker
from lonely_eye.workers.schemas import WorkerLogin, WorkerJWT
from lonely_eye.auth import utils as auth_utils
from lonely_eye.auth import dependencies as auth_dependencies


http_bearer = HTTPBearer()


async def verify_login(
    worker_login: WorkerLogin,
    session: AsyncSession = Depends(database.session_dependency),
):
    worker: Worker = await service.get_worker(
        username=worker_login.username,
        session=session,
    )

    if not auth_utils.verify_password(
        password=worker_login.password,
        hashed_password=worker.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    if worker.is_active:
        return worker

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Worker inactive",
    )


async def verify_refresh(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> WorkerJWT:

    token = credentials.credentials
    data = auth_dependencies.get_data_from_token(token)
    data["id"] = data.pop("sub")

    if data.get("token_id") is not None:
        return WorkerJWT(**data)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Wrong JWT-Token",
    )


async def verify_worker(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> AccessToken:

    access_token = credentials.credentials
    data = auth_dependencies.get_data_from_token(access_token)

    if "token_id" not in data.keys():
        return AccessToken(**data)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Wrong JWT-Token",
    )
