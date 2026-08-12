from sqlalchemy.orm import Session
from repositories import maintenance_subcategory_repository
from schemas.maintenance_subcategory import MaintenanceSubcategoryUpdate, MaintenanceSubcategoryCreate, MaintenanceSubcategoryResponse
from fastapi import HTTPException, status
from database.models import MaintenanceSubcategory

def get_all_maintenance_subcategory(db: Session):
    return maintenance_subcategory_repository.get_all_maintenance_subcategories(db)

def get_maintenance_subcategory(db: Session, subCategory_id: int):
    return maintenance_subcategory_repository.get_maintenance_subcategory(db, subCategory_id)

def create_maintenance_subcategory(db: Session, newSubcategory: MaintenanceSubcategoryCreate):
    subcategory = maintenance_subcategory_repository.get_maintenance_subcategory_by_name(db, newSubcategory.maintenance_subcategory_name)
    if subcategory is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Maintenance subcategory is not found")
    newSubcategory = MaintenanceSubcategory(
        maintenance_subcategory_name = newSubcategory.maintenance_subcategory_name,
        maintenance_category_id = newSubcategory.maintenance_category_id
    )
    return maintenance_subcategory_repository.create_maintenance_subcategory(db, newSubcategory)

def update_maintenance_subcategory(db: Session, updateSubcategory: MaintenanceSubcategoryUpdate, subCategory_id: int):
    subcategory = maintenance_subcategory_repository.get_maintenance_subcategory(db, subCategory_id)
    if subcategory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Maintenance subcategory is not found")
    if updateSubcategory.maintenance_subcategory_name is not None:
        subcategory.maintenance_subcategory_name = updateSubcategory.maintenance_subcategory_name

    return maintenance_subcategory_repository.update_maintenance_subcategory(db, subcategory)

def delete_maintenance_subcategory(db: Session, subcategory_id: int):
    subcategory = maintenance_subcategory_repository.get_maintenance_subcategory(db, subcategory_id)
    if subcategory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Maintenance subcategory is not found")

    return maintenance_subcategory_repository.delete_maintenance_subcategory(db, subcategory)