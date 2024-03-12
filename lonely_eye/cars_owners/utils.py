import io
from typing import Any

from fastapi import HTTPException, status

import openpyxl
from openpyxl.workbook import Workbook
from fastapi import UploadFile
from pydantic import ValidationError

from lonely_eye.cars_owners.schemas import CarOwner


async def get_cars_owners_from_excel(excel: UploadFile) -> list[CarOwner]:
    wb = await parce_excel(excel)
    data = _get_data_from_excel_sheet(wb=wb)

    if sorted(data[0]) != sorted(CarOwner.values()):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Expected fields: {CarOwner.values()}. Received fields: {data[0]}",
        )

    wrong_line: int = 0
    try:
        schemas: list = []
        for i in range(1, len(data)):
            d: dict = {}
            wrong_line = i
            for j in range(len(data[i])):
                if data[i][j] is None:
                    continue
                d[data[0][j]] = str(data[i][j])
            schemas.append(CarOwner.parse_obj(d))
        return schemas

    except ValidationError as ex:
        wrong_field = str(ex).split("\n")[1]
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invalid {wrong_field}: {data[wrong_line]}",
        )


def _get_data_from_excel_sheet(wb: Workbook) -> list[list[Any]]:
    ws = wb.active
    l: list = []
    for cells in ws.iter_rows():
        l.append([cell.value for cell in cells])
    return l


async def parce_excel(excel) -> Workbook:
    file = await excel.read()
    xlsx = io.BytesIO(file)
    wb = openpyxl.load_workbook(xlsx)
    return wb
