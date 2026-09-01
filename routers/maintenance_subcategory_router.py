from fastapi import status, APIRouter, Depends
from services import maintenance_subcategory
from schemas.maintenance_subcategory import MaintenanceSubcategoryCreate, MaintenanceSubcategoryUpdate, MaintenanceSubcategoryResponse
from database.database import get_db
from typing import List
from sqlalchemy.orm import Session
from database.models import User
from role_permissions import require_permission
router = APIRouter()

@router.get("/maintenance-subcategories",response_model= List[MaintenanceSubcategoryResponse],tags = ["Maintenance Subcategories"])
def get_all_maintenance_subcategory(db: Session = Depends(get_db), current_user: User = Depends(require_permission("maintenance_subcategory:read"))):
    return maintenance_subcategory.get_all_maintenance_subcategory(db)

@router.get("/maintenance-subcategories/{subcategory_id}", response_model= MaintenanceSubcategoryResponse, tags = ["Maintenance Subcategories"])
def get_maintenance_subcategory(subcategory_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_permission("maintenance_subcategory:read"))):
    return maintenance_subcategory.get_maintenance_subcategory(db, subcategory_id)

@router.post("/maintenance-subcategories", response_model=MaintenanceSubcategoryResponse, status_code=status.HTTP_201_CREATED, tags = ["Maintenance Subcategories"])
def create_maintenance_subcategory(newSubcategory: MaintenanceSubcategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("maintenance_subcategory:create"))):
    return maintenance_subcategory.create_maintenance_subcategory(db, newSubcategory)

@router.patch("/maintenance-subcategories/{subcategory_id}", response_model=MaintenanceSubcategoryResponse, status_code=status.HTTP_200_OK, tags = ["Maintenance Subcategories"])
def update_maintenance_subcategory(subcategory_id: int, updateSubcategory: MaintenanceSubcategoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("maintenance_subcategory:update"))):
    return maintenance_subcategory.update_maintenance_subcategory(db, updateSubcategory, subcategory_id)

@router.delete("/maintenance-subcategories/{subcategory_id}", status_code=status.HTTP_204_NO_CONTENT, tags = ["Maintenance Subcategories"])
def delete_maintenance_subcategory(subcategory_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_permission("maintenance_subcategory:delete"))):
    return maintenance_subcategory.delete_maintenance_subcategory(db, subcategory_id)