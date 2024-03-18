import json

from httpx import AsyncClient
from sqlalchemy import update

from lonely_eye import Worker
from lonely_eye.auth.utils import decode_jwt
from tests.conftest import async_session_maker

user_Vladimir: dict = {
    "username": "Vladimir",
    "email": "vladimir@mail.com",
    "password": "vladimir12345",
}
user_Domitry: dict = {
    "username": "Domitry",
    "email": "domytrus@mail.com",
    "password": "domitrus54321",
}
ACCESS_TOKEN: str
REFRESH_TOKEN: str


async def test_registration(ac: AsyncClient):
    data: dict = {"data": json.dumps(user_Vladimir)}
    files: dict = {"photo": open("./tests/camera_photos/high_speed.jpg", "rb")}
    response = await ac.post(
        "/workers/registration",
        data=data,
        files=files,
    )

    assert response.status_code == 201
    assert response.json() == {"username": "Vladimir", "email": "vladimir@mail.com"}


async def test_registration_duplicate(ac: AsyncClient):
    data: dict = {"data": json.dumps(user_Vladimir)}
    files: dict = {"photo": open("./tests/camera_photos/high_speed.jpg", "rb")}
    response = await ac.post(
        "/workers/registration",
        data=data,
        files=files,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Worker already exists"


async def test_login_invalid_username(ac: AsyncClient):
    response = await ac.post(
        "/workers/login",
        json={
            "username": "Vladomer",
            "password": user_Vladimir.get("password"),
        },
    )

    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]


async def test_login_invalid_password(ac: AsyncClient):
    response = await ac.post(
        "/workers/login",
        json={
            "username": user_Vladimir.get("username"),
            "password": "12345",
        },
    )

    assert response.status_code == 401
    assert "Invalid username or password" in response.json()["detail"]


async def test_login_worker_inactive(ac: AsyncClient):
    response = await ac.post(
        "/workers/login",
        json={
            "username": user_Vladimir.get("username"),
            "password": user_Vladimir.get("password"),
        },
    )

    assert response.status_code == 403
    assert "Worker inactive" in response.json()["detail"]


async def test_activate_worker():
    async with async_session_maker() as session:
        stmt = (
            update(Worker)
            .values(is_active=True)
            .where(Worker.username == user_Vladimir.get("username"))
        )
        await session.execute(stmt)
        await session.commit()


async def test_login(ac: AsyncClient):
    global ACCESS_TOKEN, REFRESH_TOKEN
    response = await ac.post(
        "/workers/login",
        json={
            "username": user_Vladimir.get("username"),
            "password": user_Vladimir.get("password"),
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json().keys()
    assert "refresh_token" in response.json().keys()

    ACCESS_TOKEN = response.json()["access_token"]
    REFRESH_TOKEN = response.json()["refresh_token"]


async def test_refresh_use_access_token(ac: AsyncClient):
    response = await ac.post(
        "/workers/refresh",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )

    assert response.status_code == 400
    assert "Wrong JWT-Token" in response.json()["detail"]


async def test_refresh(ac: AsyncClient):
    global ACCESS_TOKEN, REFRESH_TOKEN
    response = await ac.post(
        "/workers/refresh",
        headers={"Authorization": f"Bearer {REFRESH_TOKEN}"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert (
        user_Vladimir.get("username")
        in decode_jwt(response.json()["access_token"])["username"]
    )

    ACCESS_TOKEN = response.json()["access_token"]
    REFRESH_TOKEN = response.json()["refresh_token"]


async def test_logout(ac: AsyncClient):
    response = await ac.post(
        "/workers/logout",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    assert response.status_code == 200


async def test_refresh_token_after_logout(ac: AsyncClient):
    response = await ac.post(
        "/workers/refresh",
        headers={"Authorization": f"Bearer {REFRESH_TOKEN}"},
    )
    assert response.status_code == 403
    assert "Refresh-Token invalid" in response.json()["detail"]


async def test_me(ac: AsyncClient):
    response = await ac.post(
        "/workers/me",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    assert response.json()["success"]["username"] == user_Vladimir.get("username")
    assert response.status_code == 200


async def test_registration_2(ac: AsyncClient):
    data: dict = {"data": json.dumps(user_Domitry)}
    files: dict = {"photo": open("./tests/camera_photos/high_speed.jpg", "rb")}
    response = await ac.post(
        "/workers/registration",
        data=data,
        files=files,
    )

    assert response.status_code == 201
    assert response.json() == {"username": "Domitry", "email": "domytrus@mail.com"}
