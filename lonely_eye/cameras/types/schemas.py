import uuid

from datetime import datetime
from pydantic import BaseModel
from typing_extensions import TypedDict


class CameraUnified(BaseModel):
    transport_number: str
    camera_id: uuid.UUID
    violation_id: uuid.UUID
    violation_value: str
    skill_value: int
    datetime: datetime


class Camera1(BaseModel):
    type: int = 1
    transport_chars: str
    transport_numbers: str
    transport_region: str
    camera_id: uuid.UUID
    violation_id: uuid.UUID
    violation_value: str
    skill_value: int
    datetime: datetime


class Camera2Transport(TypedDict):
    chars: str
    numbers: str
    region: str


class Camera2Camera(TypedDict):
    id: uuid.UUID


class Camera2Violation(TypedDict):
    id: uuid.UUID
    value: str


class Camera2Skill(TypedDict):
    value: int


class Camera2Datetime(TypedDict):
    year: int
    month: int
    day: int
    hour: int
    minute: int
    seconds: int
    utc_offset: str


class Camera2(BaseModel):
    type: int = 2
    transport: Camera2Transport
    camera: Camera2Camera
    violation: Camera2Violation
    skill: Camera2Skill
    datetime: Camera2Datetime


class Camera3Camera(TypedDict):
    id: uuid.UUID


class Camera3Violation(TypedDict):
    id: uuid.UUID
    value: str


class Camera3(BaseModel):
    type: int = 3
    transport: str
    camera: Camera3Camera
    violation: Camera3Violation
    skill: int
    datetime: datetime
