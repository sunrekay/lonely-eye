import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from lonely_eye.models import Base
from lonely_eye.violations.constants import TYPE_LEN


class Violation(Base):
    __tablename__ = "violation"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(String(TYPE_LEN), unique=True)
    price: Mapped[int]
