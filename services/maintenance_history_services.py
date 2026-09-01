from repositories import maintenance_history_repository
from schemas.maintenance_history import ManualMaintenanceCreate, ManualMaintenanceUpdate
from database.models import MaintenanceHistory
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from typing import List

def create_manual_maintenance(db: Session, vehicle_id: int, newMaintenance: ManualMaintenanceCreate) -> MaintenanceHistory:
    history_entry = MaintenanceHistory(
        vehicle_id = vehicle_id,
        ticket_id = None,
        title = None,
        description = None,
        price = newMaintenance.price,
        maintenance_category_id = newMaintenance.maintenance_category_id,
        maintenance_subcategory_id = newMaintenance.maintenance_subcategory_id,
        created_at = newMaintenance.created_at or date.today()
    )
    return maintenance_history_repository.create_manual_maintenance(db, history_entry)

def update_manual_maintenance(db: Session, maintenance_id: int, vehicle_id: int, updateMaintenance: ManualMaintenanceUpdate,) -> MaintenanceHistory:
    maintenance = maintenance_history_repository.get_maintenance_by_maintenance_id(db, maintenance_id, vehicle_id)
    if not maintenance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "No maintenance with ID found")
    updated = updateMaintenance.model_dump(exclude_unset=True)
    for key, value in updated.items():
        setattr(maintenance, key, value)
    return maintenance_history_repository.update_manual_maintenance(db, maintenance)

def delete_manual_maintenance(db: Session, maintenance_id: int, vehicle_id: int) -> None:
    maintenance = maintenance_history_repository.get_maintenance_by_maintenance_id(db, maintenance_id, vehicle_id)
    if not maintenance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No maintenance record found with this ID"
        )
    return maintenance_history_repository.delete_manual_maintenance(db, maintenance)

def get_maintenance_history_by_vehicle_id(db: Session, vehicle_id: int):
    return maintenance_history_repository.get_maintenance_history_by_vehicle_id(db, vehicle_id)
    