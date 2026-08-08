from sqlalchemy.orm import Session
from sqlalchemy import select
from repositories import driver_user_repository
from database.models import Driver, User
from schemas.drivers import DriverCreate, DriverResponse, DriverUpdate
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


def create_driver(db: Session, newDriver: DriverCreate):
    user = db.get(User, newDriver.user_id)
    if not User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    existing_driver = (
        db.query(Driver).filter(Driver.user_id == newDriver.user_id).first()
    )
    if existing_driver:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already is a driver"
        )

    newdriver = Driver(**newDriver.model_dump())

    return driver_user_repository.create_driver(db, newdriver)


def update_driver(db: Session, updateDriver: DriverUpdate, driver_id: int):
    driver = driver_user_repository.get_driver(db, driver_id)
    if driver is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Driver not found"
        )

    if updateDriver.license_number is not None:
        driver.license_number = updateDriver.license_number
    if updateDriver.license_expire is not None:
        driver.license_expire = updateDriver.license_expire
    if updateDriver.driving_record_check is not None:
        driver.driving_record_check = updateDriver.driving_record_check
    if updateDriver.own_car is not None:
        driver.own_car = updateDriver.own_car
    if updateDriver.assigned_vehicle_check is not None:
        driver.assigned_vehicle_check = updateDriver.assigned_vehicle_check
    if updateDriver.assigned_vehicle_id is not None:
        driver.assigned_vehicle_id = updateDriver.assigned_vehicle_id
    if updateDriver.vehicle_record_check is not None:
        driver.vehicle_record_check = updateDriver.vehicle_record_check
    if updateDriver.vehicle_registeration is not None:
        driver.vehicle_registeration = updateDriver.vehicle_registeration
    if updateDriver.vehicle_last_oil_meter is not None:
        driver.vehicle_last_oil_meter = updateDriver.vehicle_last_oil_meter

    return driver_user_repository.update_driver(db, driver)


def delete_driver(db: Session, driver_id: int):
    return driver_user_repository.delete_driver(db, driver_id)
