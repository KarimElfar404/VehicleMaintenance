from pydantic import BaseModel
from enum import Enum


class VehicleStatus(str, Enum):
    ACTIVE = "active"
    MAINTENANCE = "maintenance"
    INACTIVE = "inactive"


class VehicleAssigned(str, Enum):
    ASSIGNED = "assigned"
    NOT_ASSIGNED = "unassigned"


class VehicleCreate(BaseModel):
    vehicle_make: str
    vehicle_model: str
    vehicle_color: str
    vehicle_year: int
    vehicle_plate_number: str
    vehicle_status: VehicleStatus = VehicleStatus.ACTIVE
    vehicle_assigned: VehicleAssigned = VehicleAssigned.NOT_ASSIGNED
    vehicle_current_mileage: int
    vehicle_fuel_type: str
    vehicle_record_check: bool
    vehicle_registeration: str
    vehicle_last_oil_meter: int
    assigned_driver_id: int | None = None


class VehicleResponse(BaseModel):
    id: int
    vehicle_make: str
    vehicle_model: str
    vehicle_color: str
    vehicle_year: int
    vehicle_plate_number: str
    vehicle_status: VehicleStatus = VehicleStatus.ACTIVE
    vehicle_assigned: VehicleAssigned = VehicleAssigned.NOT_ASSIGNED
    vehicle_current_mileage: int
    vehicle_fuel_type: str
    vehicle_record_check: bool
    vehicle_registeration: str
    vehicle_last_oil_meter: int
    assigned_driver_id: int | None = None

    class Config:
        from_attributes = True


class VehicleUpdate(BaseModel):
    vehicle_make: str | None = None
    vehicle_model: str | None = None
    vehicle_color: str | None = None
    vehicle_year: int | None = None
    vehicle_plate_number: str | None = None
    vehicle_status: VehicleStatus | None = None
    vehicle_assigned: VehicleAssigned | None = None
    vehicle_current_mileage: int | None = None
    vehicle_fuel_type: str | None = None
    vehicle_record_check: bool | None = None
    vehicle_registeration: str | None = None
    vehicle_last_oil_meter: int | None = None
    assigned_driver_id: int | None = None
