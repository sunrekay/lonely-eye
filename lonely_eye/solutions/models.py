from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lonely_eye.models import Base


class Solution(Base):
    __tablename__ = "solution"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    case_id: Mapped[int] = mapped_column(ForeignKey("case.id"))
    worker_id: Mapped[int] = mapped_column(ForeignKey("worker.id"))

    skill: Mapped[int] = mapped_column()
    status: Mapped[bool] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
