from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye.cases.schemas import CreateCase
from lonely_eye.cases.models import Case


async def create_case(
    create_in: CreateCase,
    session: AsyncSession,
) -> Case:
    case: Case = Case(**create_in.dict())
    session.add(case)
    await session.commit()
    return case
