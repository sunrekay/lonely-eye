from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye.cameras import service
from lonely_eye.database import database
from lonely_eye.cameras.schemas import CameraRegistration, CamRegRes

router = APIRouter(tags=["Cameras"], prefix="/cameras")


@router.post(
    "/registration",
    response_model=CamRegRes,
    status_code=status.HTTP_201_CREATED,
)
async def camera_registration(
    camera: CameraRegistration,
    session: AsyncSession = Depends(database.session_dependency),
):
    return await service.camera_registration(camera_in=camera, session=session)
