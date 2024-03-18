from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status, UploadFile, Header, Body
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye.cameras import service
from lonely_eye.database import database
from lonely_eye.cameras.schemas import CameraRegistrationIn, CameraRegistrationOut
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
