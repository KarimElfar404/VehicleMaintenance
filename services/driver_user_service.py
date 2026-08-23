from sqlalchemy.orm import Session
from repositories import driver_user_repository, vehicle_repository
from database.models import Driver, User, VehicleAssigned
from schemas.drivers import DriverCreate, DriverUpdate
from fastapi import HTTPException, status


def get_all_drivers(db: Session):
    return driver_user_repository.get_all_drivers(db)


def get_driver(db: Session, driver_id: int):
    driver = driver_user_repository.get_driver(db, driver_id)
    if driver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found"
        )

    return driver


def update_driver(db: Session, update_data: DriverUpdate, driver_id: int):
    driver = driver_user_repository.get_driver(db, driver_id)
    if driver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found"
        )

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
                    Driver.id != driver_id,
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
        if key != "assigned_vehicle_id":
            setattr(driver, key, value)

    return driver_user_repository.update_driver(db, driver)


def delete_driver(db: Session, driver_id: int):
    return driver_user_repository.delete_driver(db, driver_id)
