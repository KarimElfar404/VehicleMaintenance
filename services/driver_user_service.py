from sqlalchemy.orm import Session
from repositories import driver_user_repository, vehicle_repository
from database.models import Driver, User, VehicleAssigned
from schemas.drivers import DriverUpdate, DriverResponse
from fastapi import HTTPException, status


def get_all_drivers(db: Session):
    users = driver_user_repository.get_all_drivers(db)
    return [DriverResponse.from_user_model(user) for user in users]


def get_driver(db: Session, user_id: int):
    user = driver_user_repository.get_driver_by_user_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found"
        )

    return DriverResponse.from_user_model(user)


def update_driver(db: Session, update_data: DriverUpdate, user_id: int):
    user = driver_user_repository.get_driver_by_user_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found"
        )
    driver = driver_user_repository.create_driver(db, user)
    if update_data.assigned_vehicle_id is not None:
        if update_data.assigned_vehicle_id != driver.assigned_vehicle_id:
            vehicle = vehicle_repository.get_vehicle(
                db, update_data.assigned_vehicle_id
            )
            if not vehicle:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Vehicle not found"
                )

            existing_assigned = (
                db.query(Driver)
                .filter(
                    Driver.assigned_vehicle_id == update_data.assigned_vehicle_id,
                    Driver.id != driver.id,
                )
                .first()
            )
            if existing_assigned:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Vehicle is already assigned to another driver",
                )

            if driver.assigned_vehicle_id:
                old_vehicle = vehicle_repository.get_vehicle(
                    db, driver.assigned_vehicle_id
                )
                if old_vehicle:
                    old_vehicle.vehicle_assigned = VehicleAssigned.NOT_ASSIGNED

            vehicle.vehicle_assigned = VehicleAssigned.ASSIGNED
            driver.assigned_vehicle_id = update_data.assigned_vehicle_id
            driver.assigned_vehicle_check = True

    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        if key in ("name","email"):
            setattr(user,key,value)
        elif key != "assigned_vehicle_id":
            setattr(driver,key,value)
    updated_user = driver_user_repository.update_driver(db, user)

    return DriverResponse.from_user_model(updated_user)


def delete_driver(db: Session, driver_id: int):
    return driver_user_repository.delete_driver(db, driver_id)
