from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from typing import Optional
from enum import Enum


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
        ForeignKey("vehicles.id", ondelete="SET NULL"), nullable=True
    )
    vehicle: Mapped[Optional["Vehicle"]] = relationship(
        "Vehicle", back_populates="assigned_driver"
    )


class VehicleStatus(str, Enum):
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    INACTIVE = "inactive"


class VehicleAssigned(str, Enum):
    ASSIGNED = "assigned"
    NOT_ASSIGNED = "unassigned"


class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_make: Mapped[str] = mapped_column(nullable=False)
    vehicle_model: Mapped[str] = mapped_column(nullable=False)
    vehicle_color: Mapped[str] = mapped_column(nullable=False)
    vehicle_year: Mapped[int] = mapped_column(nullable=False)
    vehicle_plate_number: Mapped[str] = mapped_column(nullable=False)
    vehicle_status: Mapped[VehicleStatus] = mapped_column(
        default=VehicleStatus.ACTIVE, nullable=False
    )
    vehicle_assigned: Mapped[VehicleAssigned] = mapped_column(
        default=VehicleAssigned.NOT_ASSIGNED, nullable=False
    )
    vehicle_current_mileage: Mapped[int] = mapped_column(nullable=False)
    vehicle_fuel_type: Mapped[str] = mapped_column(nullable=False)
    vehicle_record_check: Mapped[bool] = mapped_column(default=False, nullable=False)
    vehicle_registeration: Mapped[str] = mapped_column(nullable=False)
    vehicle_last_oil_meter: Mapped[int] = mapped_column(nullable=False)
    assigned_driver: Mapped[Optional["Driver"]] = relationship(
        "Driver", back_populates="vehicle", uselist=False
    )

class MaintenanceCategory(Base):
    __tablename__ = "maintenance_categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    maintenance_category_name: Mapped[str] = mapped_column(nullable=False)
    maintenance: Mapped[list["MaintenanceSubcategory"]] = relationship(back_populates="maintenancecategory")

class MaintenanceSubcategory(Base):
    __tablename__ = "maintenances"

    id: Mapped[int] = mapped_column(primary_key=True)
    maintenance_subcategory_name: Mapped[str] = mapped_column(nullable=False)
    maintenancecategory: Mapped["MaintenanceCategory"] = relationship(back_populates="maintenance")
    maintenance_category_id: Mapped[int] = mapped_column(ForeignKey("maintenance_categories.id"), nullable=False)