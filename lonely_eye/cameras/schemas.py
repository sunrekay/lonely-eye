import uuid
from typing import Annotated

from annotated_types import MaxLen, Gt, Lt
from pydantic import BaseModel
from pydantic_extra_types.coordinate import Longitude, Latitude


class CameraRegistration(BaseModel):
    type: Annotated[int, Gt(0), Lt(40)]
    longitude: Longitude
    latitude: Latitude
    description: Annotated[str, MaxLen(750)]


class CamRegRes(CameraRegistration):
    key: uuid.UUID


class UploadCase(BaseModel):
    data: str
