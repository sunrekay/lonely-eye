import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lonely_eye.models import Base
from lonely_eye.violations.constants import TYPE_LEN
from lonely_eye.cases.models import Case


class Violation(Base):
    __tablename__ = "violation"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = mapped_column(String(TYPE_LEN), unique=True)
    price: Mapped[int]

    case: Mapped["Case"] = relationship(back_populates="violation")
