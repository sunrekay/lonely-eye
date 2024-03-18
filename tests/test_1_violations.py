from httpx import AsyncClient
from sqlalchemy import insert

from lonely_eye import Manager
from tests.conftest import async_session_maker
from lonely_eye.auth import utils as auth_utils

manager_Jora: dict = {
    "username": "BigBossCarOwner",
    "password": "MyLittlePony",
}
ACCESS_TOKEN: str
REFRESH_TOKEN: str


async def test_create_manager(ac: AsyncClient):
    data: dict = {}
    async with async_session_maker() as session:
        data["username"] = manager_Jora["username"]
        data["password"] = auth_utils.hash_password(manager_Jora["password"])
        await session.execute(insert(Manager).values(**data))
        await session.commit()

    global ACCESS_TOKEN, REFRESH_TOKEN
    response = await ac.post(
        "/managers/login",
        json={
            "username": manager_Jora.get("username"),
            "password": manager_Jora.get("password"),
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json().keys()
    assert "refresh_token" in response.json().keys()

    ACCESS_TOKEN = response.json()["access_token"]
    REFRESH_TOKEN = response.json()["refresh_token"]


async def test_upload_excel_invalid_xlsx(ac: AsyncClient):
    files = {
        "excel_file": open("./tests/violations_files/invalid.docx", "rb"),
    }
    response = await ac.post(
        "/violations/upload_excel",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
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
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
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
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
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
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
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
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        files=files,
    )
    assert response.status_code == 201
    assert len(response.json()["uploaded"]) == 1
