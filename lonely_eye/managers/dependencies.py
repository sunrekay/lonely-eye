from typing import Type

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye import Manager
from lonely_eye.database import database
from lonely_eye.managers import service
from lonely_eye.managers.schemas import ManagerLogin, ManagerJWT
from lonely_eye.auth import utils as auth_utils
from lonely_eye.auth import exceptions as auth_exceptions
from lonely_eye.auth import dependencies as auth_dependencies


http_bearer = HTTPBearer()


async def verify_login(
    manager_login: ManagerLogin,
    session: AsyncSession = Depends(database.session_dependency),
) -> Manager:
    manager: Manager = await service.get_manager(
        manager_login=manager_login,
        session=session,
    )
    if not auth_utils.verify_password(
        password=manager_login.password,
        hashed_password=manager.password,
    ):
        raise auth_exceptions.wrong_login_password

    return manager


async def verify_refresh(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = credentials.credentials
    data = auth_dependencies.get_data_from_token(token)
    data["id"] = data.pop("sub")

    if data.get("token_id") is not None:
        return ManagerJWT(**data)

    raise auth_exceptions.wrong_token


async def verify_manager(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(database.session_dependency),
) -> Type[Manager]:

    access_token = credentials.credentials
    data = auth_dependencies.get_data_from_token(access_token)

    if "token_id" in data.keys():
        raise auth_exceptions.wrong_token

    manager = await session.get(Manager, data["sub"])

    if manager is not None:
        return manager

    raise auth_exceptions.permission_denied
