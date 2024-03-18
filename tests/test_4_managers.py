import time

from httpx import AsyncClient
from sqlalchemy import insert

from lonely_eye import Manager
from lonely_eye.auth import utils as auth_utils
from lonely_eye.auth.utils import decode_jwt
from tests.conftest import async_session_maker


manager_Jora: dict = {
    "username": "BigBoss",
    "password": "MyLittlePony",
}
ACCESS_TOKEN: str
REFRESH_TOKEN: str


async def test_create_manager():
    data: dict = {}
    async with async_session_maker() as session:
        data["username"] = manager_Jora["username"]
        data["password"] = auth_utils.hash_password(manager_Jora["password"])
        await session.execute(insert(Manager).values(**data))
        await session.commit()


async def test_login_invalid_username(ac: AsyncClient):
    response = await ac.post(
        "/managers/login",
        json={
            "username": "Vladomer",
            "password": manager_Jora.get("password"),
        },
    )

    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]


async def test_login_invalid_password(ac: AsyncClient):
    response = await ac.post(
        "/managers/login",
        json={
            "username": manager_Jora.get("username"),
            "password": "12345",
        },
    )

    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]


async def test_login(ac: AsyncClient):
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


async def test_refresh_use_access_token(ac: AsyncClient):
    response = await ac.post(
        "/managers/refresh",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )

    assert response.status_code == 400
    assert "Wrong JWT-Token" in response.json()["detail"]


async def test_refresh(ac: AsyncClient):
    global ACCESS_TOKEN, REFRESH_TOKEN
    response = await ac.post(
        "/managers/refresh",
        headers={"Authorization": f"Bearer {REFRESH_TOKEN}"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert (
        manager_Jora.get("username")
        in decode_jwt(response.json()["access_token"])["username"]
    )

    ACCESS_TOKEN = response.json()["access_token"]
    REFRESH_TOKEN = response.json()["refresh_token"]


async def test_logout(ac: AsyncClient):
    response = await ac.post(
        "/managers/logout",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    print(response.json())
    assert response.status_code == 200


async def test_refresh_token_after_logout(ac: AsyncClient):
    response = await ac.post(
        "/managers/refresh",
        headers={"Authorization": f"Bearer {REFRESH_TOKEN}"},
    )

    assert response.status_code == 403
    assert "Refresh-Token invalid" in response.json()["detail"]


async def test_activate_invalid_access_token(ac: AsyncClient):
    response = await ac.post(
        "/managers/activate_worker",
        headers={"Authorization": f"Bearer 123"},
        params={"username": "sda"},
    )
    assert "Token invalid" in response.json()["detail"]
    assert response.status_code == 400


async def test_activate_invalid_worker(ac: AsyncClient):
    response = await ac.post(
        "/managers/activate_worker",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        params={"username": "sda"},
    )
    assert "Username invalid" in response.json()["detail"]
    assert response.status_code == 404


async def test_activate_worker(ac: AsyncClient):
    response = await ac.post(
        "/managers/activate_worker",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        params={"username": "Domitry"},
    )
    assert response.json()["status"] == "SUCCESS"
    assert response.status_code == 201


async def test_get_workers(ac: AsyncClient):
    response = await ac.get(
        "/managers/workers",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    assert len(response.json()) == 2
    assert "https://" in response.json()[1]["photo_url"]
    assert "Vladimir" == response.json()[0]["username"]
    assert "Domitry" == response.json()[1]["username"]
    assert response.json()[1]["is_active"]
