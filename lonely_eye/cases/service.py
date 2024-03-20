import json

from redis.asyncio import Redis
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from lonely_eye.config import settings
from lonely_eye.solutions.schemas import SolutionUpdateIn, SolutionUpdateOut
from lonely_eye.workers.models import Worker
from lonely_eye.cases.models import Case
from lonely_eye.cases import exceptions
from lonely_eye.cases.schemas import CreateCase, CaseStatus, CaseOut
from lonely_eye.cache_memory import Keys as key_generator
from lonely_eye.file_storage import service as file_storage_service
from lonely_eye.solutions import service as solutions_service


async def create_case(
    create_in: CreateCase,
    session: AsyncSession,
) -> Case:
    case: Case = Case(**create_in.dict())
    session.add(case)
    await session.commit()
    return case


async def get_case_from_pool(
    worker: Worker,
    client: Redis,
    session: AsyncSession,
):
    resolved = await solutions_service.resolved(worker, session)
    if resolved is not None:
        case: str = await client.get(
            name=key_generator.case_send_worker(
                _id=worker.id,
                username=worker.username,
            )
        )
        return CaseOut(**json.loads(case))

    case: Case = await get_case_by_skill(worker=worker, session=session)
    if case is None:
        raise exceptions.no_case

    key_photo_url = key_generator.case_photo_url(case.id, case.photo_id)
    url = await client.get(name=key_photo_url)
    if url is None:
        url = file_storage_service.get_photo_url(
            bucket_name=settings.storage.cases_photo_storage_name,
            file_name=str(case.photo_id),
        )
        await client.set(
            name=key_photo_url,
            value=url,
            ex=settings.redis.case_photo_url_expire_seconds,
        )

    solution = await solutions_service.create_solution(
        worker=worker,
        case=case,
        session=session,
    )

    case_pool_out = CaseOut(
        case_id=case.id,
        photo_url=url,
        transport_number=case.transport.number,
        violation_name=case.violation.type,
        violation_value=case.violation_value,
    )

    await client.set(
        name=key_generator.case_send_worker(
            _id=worker.id,
            username=worker.username,
        ),
        value=case_pool_out.model_dump_json(),
    )

    return case_pool_out


async def get_case_by_skill(
    worker: Worker,
    session: AsyncSession,
) -> Case | None:
    query = (
        select(Case)
        .where(
            (Case.skill == worker.skill) and (Case.status == CaseStatus.not_resolved)
        )
        .options(joinedload(Case.transport), joinedload(Case.violation))
    )
    case = await session.scalar(query)
    return case


async def update_solution(
    case_id: int,
    solution: SolutionUpdateIn,
    worker: Worker,
    client: Redis,
    session: AsyncSession,
):
    worker_key = key_generator.case_send_worker(_id=worker.id, username=worker.username)
    value = await client.get(worker_key)
    if value is None:
        raise exceptions.permission_denied

    await solutions_service.update_solution(
        case_id=case_id, solution=solution, worker=worker, session=session
    )
    await client.delete(worker_key)
    await check_case(case_id=case_id, worker=worker, session=session)
    return SolutionUpdateOut(case_id=case_id, status=solution.status)


async def check_case(
    case_id: int,
    worker: Worker,
    session: AsyncSession,
):
    solutions = await solutions_service.get_solution_by_case_id(
        case_id=case_id,
        session=session,
    )
    d: dict = {}
    for solution in solutions:
        d.setdefault(solution.skill, []).append(solution.status)

    if len(d[worker.skill]) == settings.k_workers:

        if sum(d[worker.skill]) == settings.k_workers:
            await update_case_status(
                case_id=case_id,
                case_status=CaseStatus.crime,
                session=session,
            )

        elif sum(d[worker.skill]) == 0:
            await update_case_status(
                case_id=case_id,
                case_status=CaseStatus.mistake,
                session=session,
            )

        else:
            await update_case_skill(
                case_id=case_id,
                skill=worker.skill + 1,
                session=session,
            )


async def update_case_status(
    case_id: int,
    case_status: str,
    session: AsyncSession,
):
    query = update(Case).values(status=case_status).where(Case.id == case_id)
    await session.execute(query)


async def update_case_skill(
    case_id: int,
    skill: int,
    session: AsyncSession,
):
    query = update(Case).values(skill=skill).where(Case.id == case_id)
    await session.execute(query)


async def get_case_by_id(
    case_id: int,
    session: AsyncSession,
):
    query = (
        select(Case)
        .where(Case.id == case_id)
        .options(
            joinedload(Case.transport),
            joinedload(Case.violation),
            selectinload(Case.worker),
        )
    )
    case = await session.scalar(query)
    return case
