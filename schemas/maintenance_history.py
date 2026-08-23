from pydantic import BaseModel

class MaintenanceHistoryResponse(BaseModel):
    id: int
    vehicle_id: int
    ticket_id: int
    title: str
    description: str
    price: int
    maintenance_category_name: str
    maintenance_subcategory_name: str

    class Config:
        from_attributes = True