from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models import Driver


def get_all_drivers(db: Session):
    statement = select(Driver)
    return db.execute(statement).scalars().all()


def get_driver(db: Session, driver_id: int):
    return db.get(Driver, driver_id)


def delete_driver(db: Session, driver_id: int):
    driver = db.query(Driver).filter(Driver.id == driver_id).first()
    db.delete(driver)
    db.commit()


def update_driver(db: Session, updateDriver: Driver):
    db.commit()
    db.refresh(updateDriver)
    return updateDriver
