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

router = APIRouter()


@router.get("/driver", response_model=List[DriverResponse], tags=["Drivers"])
def get_all_drivers(db: Session = Depends(get_db)):
    return driver_user_service.get_all_drivers(db)


@router.get("/driver/{driver_id}", response_model=DriverResponse, tags=["Drivers"])
def get_driver(driver_id: int, db: Session = Depends(get_db)):
    return driver_user_service.get_driver(db, driver_id)



@router.patch(
    "/driver/{driver_id}",
    response_model=DriverResponse,
    status_code=status.HTTP_200_OK,
    tags=["Drivers"],
)
def update_driver(
    driver_id: int, updateDriver: DriverUpdate, db: Session = Depends(get_db)
):
    return driver_user_service.update_driver(db, updateDriver, driver_id)


@router.delete(
    "/driver/{driver_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Drivers"]
)
def delete_driver(driver_id: int, db: Session = Depends(get_db)):
    return driver_user_service.delete_driver(db, driver_id)
