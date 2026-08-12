from sqlalchemy.orm import Session
from sqlalchemy import select
from database.models import MaintenanceSubcategory
from schemas.maintenance_subcategory import MaintenanceSubcategoryCreate, MaintenanceSubcategoryUpdate
from fastapi import HTTPException, status

def get_all_maintenance_subcategories(db: Session):
    subcategory = select(MaintenanceSubcategory)
    if subcategory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "Maintenance Subcategory is not found")
    return db.execute(subcategory).scalars().all()

def get_maintenance_subcategory(db: Session, subcategory_id: int):
    subcategory = db.get(MaintenanceSubcategory, subcategory_id)
    if subcategory is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Maintenance subcategory is not found")
    return subcategory

def get_maintenance_subcategory_by_name(db: Session, maintenance_subcategory_name: str):
    statement = (
        select(MaintenanceSubcategory)
        .where(MaintenanceSubcategory.maintenance_subcategory_name == maintenance_subcategory_name)
    )
    return db.scalar(statement)

def create_maintenance_subcategory(db: Session, newSubcategory: MaintenanceSubcategoryCreate):
    db.add(newSubcategory)
    db.commit()
    db.refresh(newSubcategory)
    return newSubcategory

def update_maintenance_subcategory(db: Session, updateSubcategory: MaintenanceSubcategoryUpdate):
    db.commit()
    db.refresh(updateSubcategory)
    return updateSubcategory

def delete_maintenance_subcategory(db: Session, delSubcategory: MaintenanceSubcategory):
    db.delete(delSubcategory)
    db.commit()
    return None
    