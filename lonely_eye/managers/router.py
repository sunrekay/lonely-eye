from fastapi import APIRouter, status, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye import Manager
from lonely_eye.auth.schemas import TokensInfo
from lonely_eye.auth import service as auth_service
from lonely_eye.cache_memory import cache_memory
from lonely_eye.cache_memory import Keys as key_generator
from lonely_eye.database import database

from lonely_eye.managers import service, dependencies
from lonely_eye.managers.schemas import ManagerJWT, ActivateWorkerOut, WorkerOut

router = APIRouter()


@router.post(
    "/login",
    response_model=TokensInfo,
    status_code=status.HTTP_200_OK,
)
async def manager_login(
    manager: Manager = Depends(dependencies.verify_login),
    client: Redis = Depends(cache_memory.pool_dependency),
):
    return await auth_service.login(
        model=manager,
        client=client,
        key_generator_func=key_generator.manager_refresh_token,
    )


@router.post(
    "/refresh",
    response_model=TokensInfo,
    status_code=status.HTTP_200_OK,
)
async def manager_refresh(
    manager_jwt: ManagerJWT = Depends(dependencies.verify_refresh),
    client: Redis = Depends(cache_memory.pool_dependency),
):
    return await auth_service.refresh(
        model=manager_jwt,
        client=client,
        key_generator_func=key_generator.manager_refresh_token,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def manager_logout(
    manager: Manager = Depends(dependencies.verify_manager),
    client: Redis = Depends(cache_memory.pool_dependency),
):
    await auth_service.logout(
        model=manager,
        client=client,
        key_generator_func=key_generator.manager_refresh_token,
    )


@router.post(
    "/activate_worker",
    response_model=ActivateWorkerOut,
    status_code=status.HTTP_201_CREATED,
)
async def activate_worker(
    username: str,
    manager: Manager = Depends(dependencies.verify_manager),
    session: AsyncSession = Depends(database.session_dependency),
):
    return await service.activate_worker(
        username=username,
        manager=manager,
        session=session,
    )


@router.get(
    "/workers",
    response_model=list[WorkerOut],
    status_code=status.HTTP_201_CREATED,
)
async def get_workers(
    manager: Manager = Depends(dependencies.verify_manager),
    client: Redis = Depends(cache_memory.pool_dependency),
    session: AsyncSession = Depends(database.session_dependency),
):
    return await service.get_workers(
        client=client,
        session=session,
    )
