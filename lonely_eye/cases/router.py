from fastapi import APIRouter, status, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye.cache_memory import cache_memory
from lonely_eye.database import database
from lonely_eye.solutions.schemas import SolutionUpdateIn, SolutionUpdateOut
from lonely_eye.workers.models import Worker
from lonely_eye.workers import dependencies as worker_dependencies
from lonely_eye.cases import service
from lonely_eye.cases.schemas import CaseOut

router = APIRouter()


@router.get(
    "/pool",
    response_model=CaseOut,
    status_code=status.HTTP_200_OK,
)
async def get_case_from_pool(
    worker: Worker = Depends(worker_dependencies.verify_worker),
    client: Redis = Depends(cache_memory.pool_dependency),
    session: AsyncSession = Depends(database.session_dependency),
):
    return await service.get_case_from_pool(
        worker=worker,
        client=client,
        session=session,
    )


@router.put(
    "/{case_id}",
    response_model=SolutionUpdateOut,
    status_code=status.HTTP_200_OK,
)
async def update_solution(
    case_id: int,
    solution: SolutionUpdateIn,
    worker: Worker = Depends(worker_dependencies.verify_worker),
    client: Redis = Depends(cache_memory.pool_dependency),
    session: AsyncSession = Depends(database.session_dependency),
):
    return await service.update_solution(
        case_id=case_id,
        solution=solution,
        worker=worker,
        client=client,
        session=session,
    )
