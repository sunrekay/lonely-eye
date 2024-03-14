from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye.cars_owners.schemas import (
    UploadOwnersOut,
    ExcelParse,
    TransportIn,
    TransportOwnersOut,
)
from lonely_eye.cars_owners.models import CarOwner, Transport
from lonely_eye.cars_owners.schemas import CarOwnerIn
from lonely_eye.excel import utils as excel_utils


async def add_cars_owners_and_transport_from_excel(
    excel: UploadFile,
    session: AsyncSession,
):
    excel_parse: list[ExcelParse] = await excel_utils.get_schemas_from_excel(
        excel=excel,
        pydantic_schema=ExcelParse,
    )
    uploaded: list = []
    duplicates: list = []
    for ep in excel_parse:
        try:
            car_owner_in = CarOwnerIn(**ep.dict())
            transport_in = TransportIn(**ep.dict())

            res = await session.scalars(
                select(Transport).where(Transport.number == transport_in.number)
            )
            if res.one_or_none() is not None:
                raise IntegrityError(
                    statement="", params="", orig=Exception
                )  # TODO: Write error

            car_owner = CarOwner(**car_owner_in.model_dump())
            session.add(car_owner)
            await session.commit()

            transport_in.car_owner_id = car_owner.id
            session.add(Transport(**transport_in.model_dump()))
            await session.commit()

            uploaded.append(TransportOwnersOut(**ep.dict()))

        except IntegrityError:
            await session.rollback()
            duplicates.append(
                TransportOwnersOut(**ep.dict())
            )  # TODO: Add Write exceptions in duplicates

    return UploadOwnersOut(
        uploaded=uploaded,
        duplicates=duplicates,
    )
