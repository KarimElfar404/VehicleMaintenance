from fastapi import Depends, APIRouter
from schemas.maintenance_cateogry import MaintenanceCategoryUpdate, MaintenanceCategoryCreate, MaintenanceCategoryResponse
from services import maintenance_category
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from fastapi import status
from database.models import User
from role_permissions import require_permission
router = APIRouter()

@router.get("/maintenance-categories", response_model=List[MaintenanceCategoryResponse], tags = ["Maintenance Categories"])
def get_all_maintenance_category(db: Session = Depends(get_db), current_user: User = Depends(require_permission("maintenance_category:read"))):
    return maintenance_category.get_all_maintenance_category(db)

@router.get("/maintenance-categories/{category_id}", response_model=MaintenanceCategoryResponse, tags = ["Maintenance Categories"])
def get_maintenance_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_permission("maintenance_category:read"))):
    return maintenance_category.get_maintenance_category(db, category_id)

@router.post("/maintenance-categories", response_model=MaintenanceCategoryResponse, status_code=status.HTTP_201_CREATED ,tags = ["Maintenance Categories"])
def create_maintenance_category(newCategory: MaintenanceCategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("maintenance_category:create"))):
    return maintenance_category.create_maintenance_category(db, newCategory)

@router.patch("/maintenance-categories/{category_id}", response_model=MaintenanceCategoryResponse, status_code=status.HTTP_200_OK, tags = ["Maintenance Categories"])
def update_maintenance_category(category_id: int, updateCategory: MaintenanceCategoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("maintenance_category:update"))):
    return maintenance_category.update_maintenance_category(db, updateCategory, category_id)

@router.delete("/maintenance-categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT, tags = ["Maintenance Categories"])
def delete_maintenance_category(category_id: int, db:Session = Depends(get_db), current_user: User = Depends(require_permission("maintenance_category:delete"))):
    return maintenance_category.delete_maintenance_category(db, category_id)