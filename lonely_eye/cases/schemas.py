import enum
import uuid

from pydantic import BaseModel


class CreateCase(BaseModel):
    transport_id: int
    violation_id: uuid.UUID
    violation_value: str
    photo_id: uuid.UUID
    skill: int
    status: str


class Status(enum.StrEnum):
    created: str = "Created"
    in_progress: str = "In progress"
    closed: str = "Closed"
