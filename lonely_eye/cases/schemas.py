import enum
import uuid

from pydantic import BaseModel

from lonely_eye.constants import HttpUrlStr


class CreateCase(BaseModel):
    transport_id: int
    violation_id: uuid.UUID
    violation_value: str
    photo_id: uuid.UUID
    skill: int
    status: str


class CaseStatus(enum.StrEnum):
    created: str = "Created"
    in_progress: str = "In progress"
    closed: str = "Closed"


class CaseOut(BaseModel):
    case_id: int
    photo_url: HttpUrlStr
    transport_number: str
    violation_name: str
    violation_value: str
