import uuid
from typing import Annotated, Optional

from annotated_types import MaxLen, Lt
from pydantic import BaseModel, ConfigDict

from lonely_eye.violations.constants import MAX_VIOLATIONS_PRICE, TYPE_LEN


class ViolationIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[uuid.UUID] = None
    type: Annotated[str, MaxLen(TYPE_LEN)]
    price: Annotated[int, Lt(MAX_VIOLATIONS_PRICE)]

    @staticmethod
    def keys() -> list:
        keys = list(ViolationIn.model_fields.keys())
        return keys


class ViolationsOut(BaseModel):
    uploaded: list[ViolationIn]
    duplicates: list[ViolationIn]
