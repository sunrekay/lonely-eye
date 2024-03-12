from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lonely_eye.models import Base


class CarOwner(Base):
    __tablename__ = "car_owner"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    phone: Mapped[str] = mapped_column(nullable=True, unique=True)
    vk: Mapped[str] = mapped_column(nullable=True, unique=True)
    telegram: Mapped[str] = mapped_column(nullable=True, unique=True)

    transport: Mapped[list["Transport"]] = relationship(back_populates="car_owner")


class Transport(Base):
    __tablename__ = "transport"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[str] = mapped_column(String(15), unique=True)
    car_owner_id: Mapped[int] = mapped_column(ForeignKey("car_owner.id"))

    car_owner: Mapped["CarOwner"] = relationship(back_populates="transport")
