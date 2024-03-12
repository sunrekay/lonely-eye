from fastapi import Depends, UploadFile
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye.cars_owners.schemas import UploadOwnersOut
from lonely_eye.cars_owners.models import CarOwner, Transport
from lonely_eye.cars_owners.schemas import CarOwner as CarOwnerSchemas
from lonely_eye.cars_owners import utils
from lonely_eye.database import database


async def add_cars_owners(
    excel: UploadFile,
    session: AsyncSession,
):  # TODO: Refactoring !!!
    cars_owners = await utils.get_cars_owners_from_excel(excel)
    upload_data: list = []
    wrong_data: list = []
    for car_owner in cars_owners:
        try:
            upload_data.append(
                await add_car_owner(
                    car_owner=car_owner,
                    session=session,
                )
            )
        except IntegrityError:
            await session.rollback()
            wrong_data.append(car_owner)

    return UploadOwnersOut(
        upload_data=upload_data,
        wrong_data=wrong_data,
    )


async def add_car_owner(
    car_owner: CarOwnerSchemas,
    session: AsyncSession,
):
    co = CarOwner(**car_owner.model_dump(exclude={"number", "car_owner_id"}))
    session.add(co)
    await session.commit()

    co = await session.get(CarOwner, co.id)
    car_owner.car_owner_id = co.id
    transport = Transport(
        **car_owner.model_dump(exclude={"phone", "vk", "telegram", "email"})
    )
    session.add(transport)
    await session.commit()
    return car_owner
