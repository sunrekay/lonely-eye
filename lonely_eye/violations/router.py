from typing import Annotated

from fastapi import APIRouter, Depends, status, UploadFile, Response
from sqlalchemy.ext.asyncio import AsyncSession

from lonely_eye import Manager
from lonely_eye.database import database
from lonely_eye.violations import service
from lonely_eye.excel import dependencies as excel_dependencies
from lonely_eye.violations.schemas import ViolationsOut
from lonely_eye.managers import dependencies as managers_dependencies


router = APIRouter()


@router.post(
    "/upload_excel",
    response_model=ViolationsOut,
    status_code=status.HTTP_201_CREATED,
)
async def upload_owners(
    response: Response,
    excel_file: Annotated[UploadFile, Depends(excel_dependencies.is_valid_excel)],
    manager: Manager = Depends(managers_dependencies.verify_manager),
    session: AsyncSession = Depends(database.session_dependency),
):
    upload_violations_out = await service.add_violations_from_excel(
        excel=excel_file,
        session=session,
    )
    if len(upload_violations_out.uploaded) == 0:
        response.status_code = status.HTTP_200_OK
    return upload_violations_out
