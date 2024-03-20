from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye.solutions.models import Solution
from lonely_eye.cases.models import Case
from lonely_eye.solutions.schemas import SolutionUpdateIn
from lonely_eye.workers.models import Worker


async def create_solution(
    worker: Worker,
    case: Case,
    session: AsyncSession,
):
    solution: Solution = Solution(
        case_id=case.id,
        skill=worker.skill,
        worker_id=worker.id,
    )
    session.add(solution)
    await session.commit()
    return solution


async def resolved(
    worker: Worker,
    session: AsyncSession,
):
    query = select(Solution).where(
        (Solution.worker_id == worker.id) and (Solution.status is None)
    )
    return await session.scalar(query)


async def update_solution(
    case_id: int,
    solution: SolutionUpdateIn,
    worker: Worker,
    session: AsyncSession,
):
    stmt = (
        update(Solution)
        .values(status=solution.status, updated_at=datetime.utcnow())
        .where(
            (Solution.worker_id == worker.id)
            and (Solution.case_id == case_id)
            and (Solution.status is None)
        )
    )
    await session.execute(stmt)
    return solution


async def get_solution_by_case_id(
    case_id: int,
    session: AsyncSession,
):
    query = select(Solution).where(
        (Solution.case_id == case_id) and (Solution.status is not None)
    )
    result = await session.execute(query)
    return result.scalars().all()
