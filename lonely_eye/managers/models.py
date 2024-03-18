import uuid

from sqlalchemy.orm import Mapped, mapped_column

from lonely_eye.models import Base


class Manager(Base):
    __tablename__ = "manager"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes] = mapped_column()
