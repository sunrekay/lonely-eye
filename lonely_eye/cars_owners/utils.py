import io
from typing import Any

from fastapi import HTTPException, status

import openpyxl
from openpyxl.workbook import Workbook
from fastapi import UploadFile
from pydantic import ValidationError

from lonely_eye.cars_owners.constants import FIELD_NAMES
from lonely_eye.cars_owners.schemas import ExcelParse


async def get_cars_owners_from_excel(excel: UploadFile) -> list[ExcelParse]:
    wb = await parce_excel(excel)
    data = _get_data_from_excel_sheet(wb=wb)

    if sorted(data[FIELD_NAMES]) != sorted(ExcelParse.keys()):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Expected fields: {ExcelParse.keys()}. Received fields: {data[0]}",
        )

    return _get_cars_owners_from_data(data=data)


def _get_cars_owners_from_data(data: list[list[Any]]) -> list[ExcelParse]:
    wrong_line: int = 0
    try:
        schemas: list = []
        for i in range(1, len(data)):
            d: dict = {}
            wrong_line = i
            for j in range(len(data[i])):
                if data[i][j] is None:
                    continue
                d[data[FIELD_NAMES][j]] = str(data[i][j])
            schemas.append(ExcelParse.parse_obj(d))
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
