from fastapi import APIRouter, Depends
from services import vehicles_service
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.vehicles import VehicleCreate, VehicleUpdate, VehicleResponse
from typing import List
from database.models import Vehicle
from fastapi import HTTPException, status

router = APIRouter()


@router.get("/vehicles", response_model=List[VehicleResponse], tags=["Vehicles"])
def get_all_vehicles(db: Session = Depends(get_db)):
    return vehicles_service.get_all_vehicle(db)


@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse, tags=["Vehicles"])
def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    return vehicles_service.get_vehicle(db, vehicle_id)


@router.post(
    "/vehicles",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Vehicles"],
)
def create_vehicle(newVehicle: VehicleCreate, db: Session = Depends(get_db)):
    return vehicles_service.create_vehicle(db, newVehicle)


@router.patch(
    "/vehicles/{vehicle_id}",
    response_model=VehicleResponse,
    status_code=status.HTTP_200_OK,
    tags=["Vehicles"],
)
def update_vehicle(
    vehicle_id: int, updateVehicle: VehicleUpdate, db: Session = Depends(get_db)
):
    return vehicles_service.update_vehicle(db, updateVehicle, vehicle_id)


@router.delete(
    "/vehicles/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Vehicles"]
)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    return vehicles_service.delete_vehicle(db, vehicle_id)
