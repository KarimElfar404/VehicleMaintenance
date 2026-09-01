from .database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Date, ARRAY, INTEGER, Float, String
from datetime import date
from sqlalchemy.orm import relationship
from typing import Optional, List
from enum import Enum


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    dob: Mapped[date] = mapped_column(Date, nullable=False)
    personal_id: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str]
    blood_type: Mapped[str] = mapped_column(nullable=False)
    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"), default=1, nullable=False
    )
    role: Mapped["Role"] = relationship(back_populates="user")
    driver_profile = relationship("Driver", back_populates="user", uselist = False)


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    user: Mapped[list["User"]] = relationship(back_populates="role")


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), unique=True, nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="driver_profile")
    license_number: Mapped[str] = mapped_column(unique=True, nullable=False)
    license_expire: Mapped[date] = mapped_column(Date, nullable=False)
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
    vehicle_year: Mapped[str] = mapped_column(nullable=False)
    vehicle_plate_number: Mapped[str] = mapped_column(unique=True,nullable=False)
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

    maintenance_history: Mapped[List["MaintenanceHistory"]] = relationship(back_populates="vehicle", cascade="all, delete-orphan")

class MaintenanceCategory(Base):
    __tablename__ = "maintenance_categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    maintenance_category_name: Mapped[str] = mapped_column(nullable=False)
    maintenance: Mapped[list["MaintenanceSubcategory"]] = relationship(back_populates="maintenancecategory")

class MaintenanceSubcategory(Base):
    __tablename__ = "maintenance_subcategories"

    id: Mapped[int] = mapped_column(primary_key=True)
    maintenance_subcategory_name: Mapped[str] = mapped_column(nullable=False)
    maintenancecategory: Mapped["MaintenanceCategory"] = relationship(back_populates="maintenance")
    maintenance_category_id: Mapped[int] = mapped_column(ForeignKey("maintenance_categories.id"), nullable=False)

class TicketStatus(str, Enum):
    OPEN = "Open"
    WAITING = "Waiting Reply"
    WAITING_FOR_CONFIRMATION = "Waiting for confirmation"
    ACCEPTED = "Accepted"
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    FIXED = "Fixed"
    CLOSED = "Closed"

class Tickets(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_status: Mapped[TicketStatus] = mapped_column(default= TicketStatus.OPEN, nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    total_price: Mapped[float] = mapped_column(Float, default = 0.0, nullable=False)

    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), nullable=False)
    items: Mapped[List["TicketItem"]] = relationship(back_populates="ticket", cascade="all, delete-orphan")



class TicketItem(Base):
    __tablename__ = "ticket_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False)
    maintenance_category_id: Mapped[int] = mapped_column(ForeignKey("maintenance_categories.id"), nullable=False)
    maintenance_subcategory_id: Mapped[int] = mapped_column(ForeignKey("maintenance_subcategories.id"), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    item_description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    ticket: Mapped["Tickets"] = relationship(back_populates="items")
    category: Mapped["MaintenanceCategory"] = relationship()
    subcategory: Mapped["MaintenanceSubcategory"] = relationship()

class MaintenanceHistory(Base):
    __tablename__ = "maintenance_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id", ondelete="CASCADE"), nullable=False)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete="CASCADE"), nullable=True)
    vehicle: Mapped["Vehicle"] = relationship(back_populates="maintenance_history")

    title: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    maintenance_category_id: Mapped[int] = mapped_column(ForeignKey("maintenance_categories.id"), nullable=False)
    maintenance_subcategory_id: Mapped[int] = mapped_column(ForeignKey("maintenance_subcategories.id"), nullable=False)

    created_at: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
