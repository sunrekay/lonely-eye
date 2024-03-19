import json
import random
import uuid

import requests
from httpx import AsyncClient

from camera_photos import (
    d1,
    d2,
    d3,
    test_camera_types,
)

CORRECT_KEY: uuid.UUID


async def test_camera_registration(ac: AsyncClient):
    global CORRECT_KEY
    response = await ac.post(
        "/cameras/registration",
        json={
            "type": 1,
            "longitude": 51.123,
            "latitude": 37.123,
            "description": "Something important",
        },
    )
    assert response.status_code == 201
    assert "key" in response.json(), "Key not in response json"
    assert "id" not in response.json(), "Id in response json"
    CORRECT_KEY = response.json()["key"]


async def test_upload_case_invalid_key(ac: AsyncClient):
    response = requests.post(
        url="https://recruit.rtuitlab.dev/serialize",
        data=json.dumps(random.choice(test_camera_types)),
    )
    bytes_line = response.content
    files: dict = {
        "photo": open("./tests/camera_photos/high_speed.jpg", "rb"),
    }
    response = await ac.post(
        "/cameras/upload_case",
        files=files,
        params={
            "bytes_line": bytes_line,
        },
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Camera-Key invalid"


async def test_upload_case_invalid_transport(ac: AsyncClient):
    d: dict = d3.copy()
    d["camera"]["id"] = CORRECT_KEY
    d["transport"] = "SDW123"
    response = requests.post(
        url="https://recruit.rtuitlab.dev/serialize",
        data=json.dumps(d),
    )
    bytes_line = response.content
    files: dict = {
        "photo": open("./tests/camera_photos/high_speed.jpg", "rb"),
    }
    response = await ac.post(
        "/cameras/upload_case",
        files=files,
        params={
            "bytes_line": bytes_line,
        },
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Transport number invalid"


async def test_upload_case_invalid_violation(ac: AsyncClient):
    d: dict = d3.copy()
    violation_correct = d3["violation"]["id"]
    d["camera"]["id"] = CORRECT_KEY
    d["violation"]["id"] = str(uuid.uuid4())
    response = requests.post(
        url="https://recruit.rtuitlab.dev/serialize",
        data=json.dumps(d),
    )
    bytes_line = response.content
    files: dict = {
        "photo": open("./tests/camera_photos/high_speed.jpg", "rb"),
    }
    response = await ac.post(
        "/cameras/upload_case",
        files=files,
        params={
            "bytes_line": bytes_line,
        },
    )
    d["violation"]["id"] = violation_correct
    assert response.status_code == 403
    assert response.json()["detail"] == "Violation id invalid"


async def test_upload_case_invalid_photo(ac: AsyncClient):
    d: dict = d3.copy()
    d["camera"]["id"] = CORRECT_KEY
    response = requests.post(
        url="https://recruit.rtuitlab.dev/serialize",
        data=json.dumps(d),
    )
    bytes_line = response.content
    files: dict = {
        "photo": open("./tests/camera_photos/not_photo.txt", "rb"),
    }
    response = await ac.post(
        "/cameras/upload_case",
        files=files,
        params={
            "bytes_line": bytes_line,
        },
    )
    assert response.status_code == 415
    assert "Expected" in response.json()["detail"]
    assert "txt" in response.json()["detail"]


async def test_upload_case(ac: AsyncClient):
    d: dict = d3.copy()
    d["camera"]["id"] = CORRECT_KEY
    response = requests.post(
        url="https://recruit.rtuitlab.dev/serialize",
        data=json.dumps(d),
    )
    bytes_line = response.content
    files: dict = {
        "photo": open("./tests/camera_photos/high_speed.jpg", "rb"),
    }
    response = await ac.post(
        "/cameras/upload_case",
        files=files,
        params={
            "bytes_line": bytes_line,
        },
    )
    print(response.json())
    assert response.status_code == 201
    assert response.json() == {"case_id": 1, "status": "Created"}
