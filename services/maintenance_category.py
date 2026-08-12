from sqlalchemy.orm import Session
from database.models import MaintenanceCategory
from schemas.maintenance_cateogry import MaintenanceCategoryCreate, MaintenanceCategoryUpdate, MaintenanceCategoryResponse
from repositories import maintenance_category_repository
from fastapi import HTTPException, status

def get_all_maintenance_category(db: Session):
    return maintenance_category_repository.get_all_maintenance_category(db)

def get_maintenance_category(db: Session, mainCategory_id: int):
    return maintenance_category_repository.get_maintenance_category(db, mainCategory_id)

def create_maintenance_category(db: Session, newCategory: MaintenanceCategoryCreate):
    subcategory = maintenance_category_repository.get_maintenance_category_by_name(db, newCategory.maintenance_category_name)
    if subcategory is not None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Maintenance category name is already created")
    newCategory = MaintenanceCategory(
        maintenance_category_name = newCategory.maintenance_category_name
    )
    return maintenance_category_repository.create_maintenance_category(db, newCategory)

def update_maintenance_category(db: Session, updateCategory: MaintenanceCategoryUpdate, category_id: int):
    category = maintenance_category_repository.get_maintenance_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Maintenance category is not found")
    if updateCategory.maintenance_category_name is not None:
        category.maintenance_category_name = updateCategory.maintenance_category_name

    return maintenance_category_repository.update_maintenance_category(db, category)

def delete_maintenance_category(db: Session, category_id: int):
    category = maintenance_category_repository.get_maintenance_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Maintenance category is not found")
    return maintenance_category_repository.delete_maintenance_category(db, category)