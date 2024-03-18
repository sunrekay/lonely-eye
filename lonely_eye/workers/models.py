import uuid

from sqlalchemy.orm import Mapped, mapped_column

from lonely_eye.models import Base


class Worker(Base):
    __tablename__ = "worker"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    photo_id: Mapped[uuid.UUID] = mapped_column(unique=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=False)
    skill: Mapped[int] = mapped_column(default=1)
