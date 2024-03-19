from typing import Annotated

from fastapi import APIRouter, Depends, status, UploadFile, Header, Body
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye.cameras import service
from lonely_eye.database import database
from lonely_eye.cameras.schemas import (
    CameraRegistrationIn,
    CameraRegistrationOut,
    UploadCaseOut,
)
from lonely_eye.image import dependencies as image_dependencies

router = APIRouter()


@router.post(
    "/registration",
    response_model=CameraRegistrationOut,
    status_code=status.HTTP_201_CREATED,
)
async def camera_registration(
    camera: CameraRegistrationIn,
    session: AsyncSession = Depends(database.session_dependency),
):
    return await service.camera_registration(camera_in=camera, session=session)


@router.post(
    "/upload_case",
    response_model=UploadCaseOut,
    status_code=status.HTTP_201_CREATED,
)
async def upload_case(
    photo: Annotated[UploadFile, Depends(image_dependencies.is_valid_photo_format)],
    bytes_line,
    session: AsyncSession = Depends(database.session_dependency),
):
    return await service.upload_case(
        photo=photo, bytes_line=bytes_line, session=session
    )
