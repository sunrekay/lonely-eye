from typing import Annotated, Optional

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr

from lonely_eye.cars_owners.constants import HttpUrlStr


class CarOwner(BaseModel):
    number: Annotated[str, MinLen(5), MaxLen(10)]
    email: Optional[EmailStr] = None
    phone: Annotated[str, MinLen(9), MaxLen(15)] = None  # TODO: Replace on Class
    vk: Optional[HttpUrlStr] = None
    telegram: Optional[HttpUrlStr] = None
    car_owner_id: Optional[int] = None  # TODO: Create new BaseModel

    @staticmethod
    def values() -> list:
        return list(CarOwner.model_fields.keys())[:-1]


class UploadOwnersOut(BaseModel):
    upload_data: Optional[list[CarOwner]] = None
    wrong_data: Optional[list[CarOwner]] = None
