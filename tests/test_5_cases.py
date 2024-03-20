from httpx import AsyncClient

user_1: dict = {
    "username": "Vladimir",
    "email": "vladimir@mail.com",
    "password": "vladimir12345",
}

ACCESS_TOKEN: str
REFRESH_TOKEN: str
CASE: dict


async def login_user(ac):
    global ACCESS_TOKEN, REFRESH_TOKEN
    response = await ac.post(
        "/workers/login",
        json={
            "username": user_1.get("username"),
            "password": user_1.get("password"),
        },
    )
    ACCESS_TOKEN = response.json()["access_token"]
    REFRESH_TOKEN = response.json()["refresh_token"]


async def test_get_case_from_pool_un_auth(ac: AsyncClient):
    await login_user(ac)
    response = await ac.get(
        "/cases/pool",
        headers={"Authorization": f"Bearer KEK"},
    )
    assert response.status_code == 400
    assert "Token invalid" in response.json()["detail"]


async def test_get_case_from_pool(ac: AsyncClient):
    global CASE
    await login_user(ac)
    response = await ac.get(
        "/cases/pool",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    assert response.status_code == 200
    assert "photo_url" in response.json().keys()
    assert "transport_number" in response.json().keys()
    assert "violation_name" in response.json().keys()
    assert "https" in response.json()["photo_url"]
    CASE = response.json()


async def test_update_case(ac: AsyncClient):
    await login_user(ac)
    payload = {"status": True}
    response = await ac.put(
        f"/cases/{CASE['case_id']}",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json=payload,
    )
    assert response.status_code == 200
    assert response.text == '{"status":true,"case_id":3}'


async def test_update_case_no_access(ac: AsyncClient):
    await login_user(ac)
    payload = {"status": True}
    response = await ac.put(
        f"/cases/{CASE['case_id']}",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json=payload,
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Permission denied"
