from sqlalchemy.orm import Session
from database.models import MaintenanceHistory
from schemas.maintenance_history import ManualMaintenanceCreate, ManualMaintenanceUpdate
from typing import List

def maintenance_entry_history(db: Session, history_entry: MaintenanceHistory) -> MaintenanceHistory:
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)
    return history_entry

def get_maintenance_history_by_vehicle_id(db: Session, vehicle_id: int) -> List[MaintenanceHistory]:
    statement = db.query(MaintenanceHistory).where(MaintenanceHistory.vehicle_id == vehicle_id).all()
    return statement

def get_maintenance_by_maintenance_id(db: Session, maintenance_id: int, vehicle_id:int):
    statement = (
        db.query(MaintenanceHistory)
        .filter(
            MaintenanceHistory.id == maintenance_id,
            MaintenanceHistory.vehicle_id == vehicle_id
        )
        .first()
    )
    return statement

def create_manual_maintenance(db: Session, createMaintenance: ManualMaintenanceCreate):
    db.add(createMaintenance)
    db.commit()
    db.refresh(createMaintenance)
    return createMaintenance

def update_manual_maintenance(db: Session, updateMaintenance: ManualMaintenanceUpdate) -> MaintenanceHistory:
    db.commit()
    db.refresh(updateMaintenance)
    return updateMaintenance

def delete_manual_maintenance(db: Session, delMaintenance: MaintenanceHistory):
    db.delete(delMaintenance)
    db.commit()
    return None

def bulk_create_maintenance_entries(db: Session, history_entries: List[MaintenanceHistory]) -> List[MaintenanceHistory]:
    db.add_all(history_entries)
    db.commit()
    return history_entries