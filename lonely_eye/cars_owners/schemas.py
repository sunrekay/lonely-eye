from typing import Annotated, Optional

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr

from lonely_eye.constants import HttpUrlStr


class CarOwnerIn(BaseModel):
    email: Optional[EmailStr]
    phone: Annotated[str, MinLen(9), MaxLen(15)]
    vk: Optional[HttpUrlStr] = None
    telegram: Optional[HttpUrlStr] = None


class TransportIn(BaseModel):
    number: Annotated[str, MinLen(5), MaxLen(10)]
    car_owner_id: Optional[int] = None


class ExcelParse(TransportIn, CarOwnerIn):
    @staticmethod
    def keys() -> list:
        keys = list(ExcelParse.model_fields.keys())
        keys.remove("car_owner_id")
        return keys


class TransportOwnersOut(CarOwnerIn):
    number: Annotated[str, MinLen(5), MaxLen(10)]


class UploadOwnersOut(BaseModel):
    uploaded: Optional[list[TransportOwnersOut]] = None
    duplicates: Optional[list[TransportOwnersOut]] = None
