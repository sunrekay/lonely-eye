import uuid

from pydantic import BaseModel


class CameraRegistration(BaseModel):
    type: int
    longitude: str
    latitude: str
    description: str


class CamRegRes(CameraRegistration):
    key: uuid.UUID
