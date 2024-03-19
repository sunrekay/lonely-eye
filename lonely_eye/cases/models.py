from datetime import datetime
from typing import TYPE_CHECKING
import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lonely_eye.models import Base

if TYPE_CHECKING:
    from lonely_eye.cars_owners.models import Transport
    from lonely_eye.violations.models import Violation


class Case(Base):
    __tablename__ = "case"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    transport_id: Mapped[int] = mapped_column(ForeignKey("transport.id"))
    violation_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("violation.id"))

    violation_value: Mapped[str] = mapped_column()
    photo_id: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4, unique=True)
    skill: Mapped[int] = mapped_column()
    status: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    transport: Mapped["Transport"] = relationship(back_populates="case")
    violation: Mapped["Violation"] = relationship(back_populates="case")


# class Solution(Base):
#     pass
