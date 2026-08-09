from sqlalchemy.orm import Session
from repositories import vehicle_repository
from schemas.vehicles import VehicleCreate, VehicleUpdate
from fastapi import HTTPException, status
from database.models import Vehicle


def get_all_vehicle(db: Session):
    vehicle = vehicle_repository.get_all_vehicle(db)
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No vehicle found"
        )
    return vehicle


def get_vehicle(db: Session, vehicle_id: int):
    vehicle = vehicle_repository.get_vehicle(db, vehicle_id)

    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found"
        )

    return vehicle


def create_vehicle(db: Session, newVehicle: VehicleCreate):
    registeredvehicle = vehicle_repository.get_vehicle_by_plate_number(
        db, newVehicle.vehicle_plate_number
    )
    if registeredvehicle is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vehicle with plate number already created",
        )
    vehicle_data = newVehicle.model_dump(exclude={"assigned_driver_id"})
    db_vehicle = Vehicle(**vehicle_data)

    return vehicle_repository.create_vehicle(db, db_vehicle)


def update_vehicle(db: Session, updateVehicle: VehicleUpdate, vehicle_id: int):
    vehicle = vehicle_repository.get_vehicle(db, vehicle_id)
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found"
        )

    update_dict = updateVehicle.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(vehicle, key, value)

    return vehicle_repository.update_vehicle(db, vehicle)


def delete_vehicle(db: Session, vehicle_id: int):
    return vehicle_repository.delete_vehicle(db, vehicle_id)
