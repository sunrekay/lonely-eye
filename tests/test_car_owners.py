from httpx import AsyncClient


async def test_upload_owners_valid_xlsx(ac: AsyncClient):
    files = {
        "excel_file": open("./tests/car_owners_files/car_owners.xlsx", "rb"),
    }
    response = await ac.post(
        "/cars_owners/upload_owners",
        files=files,
    )
    assert response.status_code == 201
    assert response.json()["status"] == "SUCCESS"


async def test_upload_owners_invalid_xlsx(ac: AsyncClient):
    files = {
        "excel_file": open("./tests/car_owners_files/car_owners_invalid.docx", "rb"),
    }
    response = await ac.post(
        "/cars_owners/upload_owners",
        files=files,
    )
    print(response.json())
    assert response.status_code == 415
    assert "detail" in response.json().keys()
