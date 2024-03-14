from httpx import AsyncClient


async def test_upload_excel_invalid_xlsx(ac: AsyncClient):
    files = {
        "excel_file": open("./tests/violations_files/invalid.docx", "rb"),
    }
    response = await ac.post(
        "/violations/upload_excel",
        files=files,
    )
    assert response.status_code == 415
    assert "detail" in response.json().keys()


async def test_upload_excel_valid_xlsx(ac: AsyncClient):
    files = {
        "excel_file": open("./tests/violations_files/valid.xlsx", "rb"),
    }
    response = await ac.post(
        "/violations/upload_excel",
        files=files,
    )
    assert response.status_code == 201
    assert len(response.json()["duplicates"]) == 0


async def test_upload_excel_valid_xlsx_invalid_fields(ac: AsyncClient):
    files = {
        "excel_file": open("./tests/violations_files/invalid_fields.xlsx", "rb"),
    }
    response = await ac.post(
        "/violations/upload_excel",
        files=files,
    )
    assert response.status_code == 409
    assert "Expected" in response.json()["detail"]


async def test_upload_excel_valid_xlsx_invalid_data(ac: AsyncClient):
    files = {
        "excel_file": open("./tests/violations_files/invalid_data.xlsx", "rb"),
    }
    response = await ac.post(
        "/violations/upload_excel",
        files=files,
    )
    assert response.status_code == 409
    assert "Invalid" in response.json()["detail"]


async def test_upload_excel_valid_xlsx_duplicates(ac: AsyncClient):
    files = {
        "excel_file": open("./tests/violations_files/valid_with_duplicates.xlsx", "rb"),
    }
    response = await ac.post(
        "/violations/upload_excel",
        files=files,
    )
    assert response.status_code == 201
    assert len(response.json()["uploaded"]) == 1
