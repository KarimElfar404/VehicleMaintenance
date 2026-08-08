from pydantic import BaseModel, EmailStr
from typing import Optional


class DriverCreate(BaseModel):
    user_id: int
    license_number: str
    license_expire: str
    driving_record_check: bool
    own_car: bool
    assigned_vehicle_check: bool
    assigned_vehicle_id: int
    vehicle_record_check: bool
    vehicle_registeration: str
    vehicle_last_oil_meter: str


class DriverUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    license_number: str | None = None
    license_expire: str | None = None
    driving_record_check: bool | None = None
    own_car: bool | None = None
    assigned_vehicle_check: bool | None = None
    assigned_vehicle_id: int | None = None
    vehicle_record_check: bool | None = None
    vehicle_registeration: str | None = None
    vehicle_last_oil_meter: str | None = None


class UserDriverResponse(BaseModel):
    id: int
    name: str
    email: str
    dob: str
    blood_type: str

    class Config:
        from_attributes = True


class DriverResponse(BaseModel):
    id: int
    user_id: int
    user: UserDriverResponse
    license_number: str
    license_expire: str
    driving_record_check: bool
    own_car: bool
    assigned_vehicle_check: bool
    assigned_vehicle_id: int
    vehicle_record_check: bool
    vehicle_registeration: str
    vehicle_last_oil_meter: str

    class Config:
        from_attributes = True
