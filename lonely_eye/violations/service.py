from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye.violations.schemas import ViolationIn, ViolationsOut
from lonely_eye.violations.models import Violation
from lonely_eye.excel import utils as excel_utils


async def add_violations_from_excel(
    excel,
    session: AsyncSession,
):
    excel_parse: list[ViolationIn] = await excel_utils.get_schemas_from_excel(
        excel=excel,
        pydantic_schema=ViolationIn,
    )
    uploaded: list[ViolationIn] = []
    duplicates: list[ViolationIn] = []

    for violation_in in excel_parse:
        try:
            violation = Violation(**violation_in.model_dump())
            session.add(violation)
            await session.commit()
            uploaded.append(ViolationIn.model_validate(violation))

        except IntegrityError:
            await session.rollback()
            duplicates.append(violation_in)

    return ViolationsOut(
        uploaded=uploaded,
        duplicates=duplicates,
    )
