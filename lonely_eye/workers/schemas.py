import json
from typing import Optional, Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict, EmailStr, model_validator

from lonely_eye.constants import HttpUrlStr


class WorkerRegistrationOut(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr


class WorkerRegistrationIn(WorkerRegistrationOut):
    password: str

    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class WorkerLogin(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: str


class WorkerJWT(BaseModel):
    id: int
    username: str
    token_id: Optional[str] = None


class WorkerSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    photo: HttpUrlStr
    username: Annotated[str, MinLen(3), MaxLen(20)]
    password: bytes
    email: Optional[EmailStr]
    active: bool = False
