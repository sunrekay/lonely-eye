from typing import Annotated

from fastapi import APIRouter, Depends, status, UploadFile, Response
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye.cars_owners.schemas import UploadOwnersOut
from lonely_eye.database import database
from lonely_eye.cars_owners import service
from lonely_eye.excel import dependencies

router = APIRouter()


@router.post(
    "/upload_excel",
    response_model=UploadOwnersOut,
    status_code=status.HTTP_201_CREATED,
)
async def upload_owners(
    response: Response,
    excel_file: Annotated[UploadFile, Depends(dependencies.is_valid_excel)],
    session: AsyncSession = Depends(database.session_dependency),
):
    upload_owners_out = await service.add_cars_owners_and_transport_from_excel(
        excel=excel_file,
        session=session,
    )
    if len(upload_owners_out.uploaded) == 0:
        response.status_code = status.HTTP_200_OK
    return upload_owners_out
