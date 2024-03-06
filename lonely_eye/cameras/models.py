import uuid

from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped, mapped_column

from lonely_eye.models import Base


class Camera(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[int] = mapped_column()
    longitude: Mapped[str] = mapped_column(String(15))
    latitude: Mapped[str] = mapped_column(String(15))
    description: Mapped[str] = mapped_column(
        Text,
        default="",
    )
    key: Mapped[uuid.UUID] = mapped_column(default=uuid.uuid4)
