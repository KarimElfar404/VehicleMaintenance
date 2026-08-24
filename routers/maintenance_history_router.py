from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from services import maintenance_history_services
from database.database import get_db
from schemas.maintenance_history import MaintenanceHistoryResponse, ManualMaintenanceCreate, ManualMaintenanceUpdate
router = APIRouter()

@router.post("/vehicles/{vehicle_id}/maintenance_history", response_model= MaintenanceHistoryResponse, status_code=status.HTTP_201_CREATED ,tags = ["Maintenance History"])
def create_manual_maintenance(vehicle_id:int, newMaintenance: ManualMaintenanceCreate, db: Session = Depends(get_db)):
    return maintenance_history_services.create_manual_maintenance(db, vehicle_id, newMaintenance)

@router.patch("/vehicles/{vehicle_id}/maintenance_history/{maintenance_id}", response_model=MaintenanceHistoryResponse, status_code=status.HTTP_200_OK, tags = ["Maintenance History"])
def update_manual_maintenance(vehicle_id:int, maintenance_id: int, updateMaintenance: ManualMaintenanceUpdate, db: Session = Depends(get_db)):
    return maintenance_history_services.update_manual_maintenance(db=db, maintenance_id=maintenance_id, vehicle_id=vehicle_id, updateMaintenance=updateMaintenance)

@router.delete("/vehicles/{vehicle_id}/maintenance_history/{maintenance_id}", status_code=status.HTTP_204_NO_CONTENT, tags = ["Maintenance History"])
def delete_manual_maintenance(vehicle_id: int, maintenance_id: int, db: Session = Depends(get_db)):
    return maintenance_history_services.delete_manual_maintenance(db=db, vehicle_id=vehicle_id, maintenance_id=maintenance_id)