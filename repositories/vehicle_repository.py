from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models import Vehicle


def get_all_vehicle(db: Session):
    statement = select(Vehicle)
    return db.execute(statement).scalars().all()


def get_vehicle(db: Session, vehicle_id: int):
    return db.get(Vehicle, vehicle_id)


def get_vehicle_by_plate_number(db: Session, vehicle_plate_number: str):
    statement = select(Vehicle).where(
        Vehicle.vehicle_plate_number == vehicle_plate_number
    )
    return db.scalar(statement)


def create_vehicle(db: Session, newVehicle: Vehicle):
    db.add(newVehicle)
    db.commit()
    db.refresh(newVehicle)
    return newVehicle


def update_vehicle(db: Session, updateVehicle: Vehicle):
    db.commit()
    db.refresh(updateVehicle)
    return updateVehicle


def delete_vehicle(db: Session, vehicle_id):
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if not vehicle:
        return None
    db.delete(vehicle)
    db.commit()
    return vehicle
