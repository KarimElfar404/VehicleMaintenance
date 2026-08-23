from sqlalchemy.orm import Session
from database.models import MaintenanceHistory
from typing import List

def maintenance_entry_history(db: Session, history_entry: MaintenanceHistory) -> MaintenanceHistory:
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)
    return history_entry

def get_maintenance_history_by_vehicle_id(db: Session, vehicle_id: int) -> List[MaintenanceHistory]:
    statement = db.query(MaintenanceHistory).where(MaintenanceHistory.vehicle_id == vehicle_id).all()
    return statement

