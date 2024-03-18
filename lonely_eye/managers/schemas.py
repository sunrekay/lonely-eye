import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr

from lonely_eye.constants import HttpUrlStr


class ManagerLogin(BaseModel):
    username: str
    password: str


class ManagerJWT(BaseModel):
    id: str
    username: str
    token_id: Optional[str] = None


class ManagerSchema(BaseModel):
    id: uuid.UUID
    username: str
    password: bytes


class ActivateWorkerOut(BaseModel):
    status: str = "SUCCESS"


class WorkerOut(BaseModel):
    photo_url: Optional[HttpUrlStr] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    skill: Optional[int] = None
    is_active: Optional[bool] = None
