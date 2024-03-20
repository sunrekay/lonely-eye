import uuid

from fastapi import UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye.cameras import utils, exceptions
from lonely_eye.cameras.models import Camera
from lonely_eye.cameras.schemas import CameraRegistrationIn, UploadCaseOut
from lonely_eye.cameras.types import CameraUnified
from lonely_eye.config import settings
from lonely_eye.violations import service as violations_service
from lonely_eye.cars_owners import service as car_owners_service
from lonely_eye.file_storage import service as file_storage_service
from lonely_eye.cases import service as cases_service
from lonely_eye.cases.schemas import CreateCase, CaseStatus


async def camera_registration(
    camera_in: CameraRegistrationIn,
    session: AsyncSession,
) -> Camera:
    camera = Camera(**camera_in.model_dump())
    session.add(camera)
    await session.commit()
    return camera


async def get_camera_by_key(
    key: uuid.UUID,
    session: AsyncSession,
) -> Camera | None:
    stmt = select(Camera).where(Camera.key == key)
    result = await session.execute(stmt)
    return result.scalar()


async def upload_case(
    photo: UploadFile,
    bytes_line: str,
    session: AsyncSession,
):
    data = utils.deserialize(eval(bytes_line)[2:])
    camera_schema = utils.get_camera_schemas(data)
    camera_unify: CameraUnified = utils.unify_camera_schema(camera_schema)

    camera = await get_camera_by_key(camera_unify.camera_id, session)
    if camera is None:
        raise exceptions.wrong_camera_key

    transport = await car_owners_service.get_transport_by_number(
        camera_unify.transport_number,
        session,
    )
    if transport is None:
        raise exceptions.wrong_transport_number

    violation = await violations_service.get_violation(
        camera_unify.violation_id, session
    )
    if violation is None:
        raise exceptions.wrong_violation_key

    photo_id = str(uuid.uuid4())
    uploaded = file_storage_service.upload_photo(
        file=photo.file,
        file_name=photo_id,
        bucket_name=settings.storage.cases_photo_storage_name,
    )
    if not uploaded:
        raise exceptions.too_many_requests

    create_case: CreateCase = CreateCase(
        transport_id=transport.id,
        violation_id=violation.id,
        violation_value=camera_unify.violation_value,
        photo_id=photo_id,
        skill=camera_unify.skill_value,
        status=CaseStatus.created,
    )

    case = await cases_service.create_case(
        create_in=create_case,
        session=session,
    )

    return UploadCaseOut(
        case_id=case.id,
        status=case.status,
    )
