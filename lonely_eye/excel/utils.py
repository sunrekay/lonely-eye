import io
from typing import Any

import openpyxl
from fastapi import HTTPException, status
from openpyxl.workbook import Workbook
from pydantic import ValidationError

from lonely_eye.excel.constants import FIELD_NAMES_INDEX


async def get_schemas_from_excel(excel, pydantic_schema: Any) -> list[Any]:
    wb = await parce(excel)
    data = get_data_from_sheet(wb=wb)

    if sorted(data[FIELD_NAMES_INDEX]) != sorted(pydantic_schema.keys()):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Expected fields: {pydantic_schema.keys()}. Received fields: {data[FIELD_NAMES_INDEX]}",
        )

    return get_schemas_from_data(
        data=data,
        pydantic_schema=pydantic_schema,
    )


async def parce(excel) -> Workbook:
    file = await excel.read()
    xlsx = io.BytesIO(file)
    work_book: Workbook = openpyxl.load_workbook(xlsx)
    return work_book


def get_data_from_sheet(wb: Workbook) -> list[list[Any]]:
    ws = wb.active
    l: list = []
    for cells in ws.iter_rows():
        l.append([cell.value for cell in cells])
    return l


def get_schemas_from_data(data: list[list[Any]], pydantic_schema: Any) -> list[Any]:
    wrong_line: int = 0
    try:
        schemas: list = []
        for i in range(1, len(data)):
            d: dict = {}
            wrong_line = i
            for j in range(len(data[i])):
                if data[i][j] is None:
                    continue
                d[data[FIELD_NAMES_INDEX][j]] = str(data[i][j])
            schemas.append(pydantic_schema.parse_obj(d))
        return schemas

    except ValidationError as ex:
        wrong_field = str(ex).split("\n")[1]
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Invalid {wrong_field}: {data[wrong_line]}",
        )
