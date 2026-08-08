from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    dob: Mapped[str] = mapped_column(nullable=False)
    personal_id: Mapped[str]
    address: Mapped[str]
    blood_type: Mapped[str] = mapped_column(nullable=False)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"), default=1, nullable=False
    )
    role: Mapped["Role"] = relationship(back_populates="user")
    driver_profile: Mapped[Optional["Driver"]] = relationship(
        back_populates="user", uselist=False
    )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True, nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="driver_profile")
    license_number: Mapped[str] = mapped_column(nullable=False)
    license_expire: Mapped[str] = mapped_column(nullable=False)
    driving_record_check: Mapped[bool] = mapped_column(nullable=False)
    own_car: Mapped[bool] = mapped_column(nullable=False)
    assigned_vehicle_check: Mapped[bool] = mapped_column(nullable=False)
    assigned_vehicle_id: Mapped[Optional[int]] = mapped_column(
        nullable=True
    )  # In future, It will be a relationship with a database class Vehicles

    vehicle_record_check: Mapped[Optional[bool]] = mapped_column(nullable=True)
    vehicle_registeration: Mapped[Optional[str]] = mapped_column(nullable=True)
    vehicle_last_oil_meter: Mapped[Optional[str]] = mapped_column(nullable=True)
