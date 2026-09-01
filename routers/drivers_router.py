from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from services import driver_user_service
from schemas.drivers import (
    DriverUpdate,
    DriverResponse,
)
from typing import List
from fastapi import status, HTTPException
from database.models import User
from role_permissions import require_permission
router = APIRouter()


@router.get("/drivers", response_model=List[DriverResponse], tags=["Drivers"])
def get_all_drivers(db: Session = Depends(get_db), current_user: User = Depends(require_permission("driver:read"))):
    return driver_user_service.get_all_drivers(db)


@router.get("/drivers/{user_id}", response_model=DriverResponse, tags=["Drivers"])
def get_driver(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_permission("driver:read"))):
    return driver_user_service.get_driver(db, user_id)



@router.patch(
    "/drivers/{user_id}",
    response_model=DriverResponse,
    status_code=status.HTTP_200_OK,
    tags=["Drivers"],
)
def update_driver(
    user_id: int, updateDriver: DriverUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("driver:update"))
):
    return driver_user_service.update_driver(db, updateDriver, user_id)


@router.delete(
    "/drivers/{driver_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Drivers"]
)
def delete_driver(driver_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_permission("driver:delete"))):
    return driver_user_service.delete_driver(db, driver_id)
