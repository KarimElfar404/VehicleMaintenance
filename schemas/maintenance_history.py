from pydantic import BaseModel
from datetime import date
class MaintenanceHistoryResponse(BaseModel):
    id: int
    vehicle_id: int
    ticket_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: float
    maintenance_category_id: int
    maintenance_subcategory_id: int
    created_at: date

    class Config:
        from_attributes = True

class ManualMaintenanceCreate(BaseModel):
    price: float
    maintenance_category_id: int
    maintenance_subcategory_id: int
    created_at: date | None = None
class ManualMaintenanceUpdate(BaseModel):
    vehicle_id: int | None = None
    title: str | None = None
    description: str | None = None
    price: float | None = None
    maintenance_category_id: int | None = None
    maintenance_subcategory_id: int | None = None