from fastapi import APIRouter, status, Depends, UploadFile
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye import Worker
from lonely_eye.auth.schemas import TokensInfo, AccessToken
from lonely_eye.cache_memory import cache_memory
from lonely_eye.database import database
from lonely_eye.workers import service, dependencies
from lonely_eye.workers.schemas import (
    WorkerRegistrationIn,
    WorkerRegistrationOut,
    WorkerJWT,
)
from lonely_eye.image import dependencies as image_dependencies

router = APIRouter()


@router.post(
    "/registration",
    response_model=WorkerRegistrationOut,
    status_code=status.HTTP_201_CREATED,
)
async def worker_registration(
    data: WorkerRegistrationIn,
    photo: UploadFile = Depends(image_dependencies.is_valid_photo_format),
    session: AsyncSession = Depends(database.session_dependency),
):
    return await service.create_worker(
        photo=photo,
        worker_in=data,
        session=session,
    )


@router.post(
    "/login",
    response_model=TokensInfo,
    status_code=status.HTTP_200_OK,
)
async def worker_login(
    worker: Worker = Depends(dependencies.verify_login),
    client: Redis = Depends(cache_memory.pool_dependency),
):
    return await service.worker_login(worker=worker, client=client)


@router.post(
    "/refresh",
    response_model=TokensInfo,
    status_code=status.HTTP_200_OK,
)
async def worker_refresh(
    worker_jwt: WorkerJWT = Depends(dependencies.verify_refresh),
    client: Redis = Depends(cache_memory.pool_dependency),
):
    return await service.worker_refresh(
        worker_jwt=worker_jwt,
        client=client,
    )


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
)
async def worker_logout(
    access_token: AccessToken = Depends(dependencies.verify_worker),
    client: Redis = Depends(cache_memory.pool_dependency),
):
    await service.worker_logout(
        access_token=access_token,
        client=client,
    )


@router.post(  # TODO: Delete router ?
    "/me",
    response_model="",
    status_code=status.HTTP_200_OK,
)
async def worker_me(
    access_token: AccessToken = Depends(dependencies.verify_worker),
):
    return {"success": access_token.model_dump()}
