import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status, Header, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye.cameras import service
from lonely_eye.database import database


async def is_valid_key(
    key: Annotated[uuid.UUID, Header(alias="API-Key")],
    session: AsyncSession = Depends(database.session_dependency),
):
    result = await service.get_camera_by_key(
        key=key,
        session=session,
    )
    if result is not None:
        return key

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Camera '{key}' not found",
    )
