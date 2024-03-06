from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye.cameras.models import Camera
from lonely_eye.cameras.schemas import CameraRegistration


async def camera_registration(
    camera_in: CameraRegistration,
    session: AsyncSession,
):
    camera = Camera(**camera_in.model_dump())
    session.add(camera)
    await session.commit()
    return await session.get(Camera, camera.id)
