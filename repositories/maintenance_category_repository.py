from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models import MaintenanceCategory
from schemas.maintenance_cateogry import MaintenanceCategoryCreate, MaintenanceCategoryUpdate
from fastapi import HTTPException, status

def get_all_maintenance_category(db: Session):
    statement = select(MaintenanceCategory)
    if statement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Maintenance Category is not found")
    return db.execute(statement).scalars().all()

def get_maintenance_category(db: Session, maincategory_id: int):
    category = db.get(MaintenanceCategory, maincategory_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

def get_maintenance_category_by_name(db: Session, maintenance_category_name: str):
    statement = (
        select(MaintenanceCategory)
        .where(MaintenanceCategory.maintenance_category_name == maintenance_category_name)
    )
    return db.scalar(statement)

def create_maintenance_category(db: Session, newCategory: MaintenanceCategoryCreate):
    db.add(newCategory)
    db.commit()
    db.refresh(newCategory)
    return newCategory

def update_maintenance_category(db: Session, updateCategory: MaintenanceCategoryUpdate):
    db.commit()
    db.refresh(updateCategory)
    return updateCategory

def delete_maintenance_category(db:Session, delCategory: MaintenanceCategory):
    db.delete(delCategory)
    db.commit()
    return None