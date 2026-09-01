from pydantic import BaseModel, EmailStr
from datetime import date
from database.models import User

class DriverUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    license_number: str | None = None
    license_expire: date | None = None
    driving_record_check: bool | None = None
    own_car: bool | None = None
    assigned_vehicle_check: bool | None = None
    assigned_vehicle_id: int | None = None


class UserDriverResponse(BaseModel):
    id: int
    name: str
    email: str
    dob: date
    blood_type: str

    class Config:
        from_attributes = True


class DriverResponse(BaseModel):
    # User details
    id: int  # maps to User.id
    name: str
    email: str
    dob: date
    blood_type: str
    driver_profile_id: int | None = None
    license_number: str | None = None
    license_expire: date | None = None
    driving_record_check: bool | None = None
    own_car: bool | None = None
    assigned_vehicle_check: bool | None = None
    assigned_vehicle_id: int | None = None

    @classmethod
    def from_user_model(cls, user: User):
        profile = user.driver_profile
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            dob=user.dob,
            blood_type=user.blood_type,
            driver_profile_id=profile.id if profile else None,
            license_number=profile.license_number if profile else None,
            license_expire=profile.license_expire if profile else None,
            driving_record_check=profile.driving_record_check if profile else None,
            own_car=profile.own_car if profile else None,
            assigned_vehicle_check=profile.assigned_vehicle_check if profile else None,
            assigned_vehicle_id=profile.assigned_vehicle_id if profile else None,
        )

    class Config:
        from_attributes = True
