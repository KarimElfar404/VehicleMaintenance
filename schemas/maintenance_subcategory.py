from pydantic import BaseModel

class MaintenanceSubcategoryCreate(BaseModel):
    maintenance_subcategory_name: str
    maintenance_category_id: int

class MaintenanceSubcategoryUpdate(BaseModel):
    maintenance_subcategory_name: str | None = None
    maintenance_category_id: int | None = None

class MaintenanceSubcategoryResponse(BaseModel):
    id: int
    maintenance_subcategory_name: str
    maintenance_category_id: int
