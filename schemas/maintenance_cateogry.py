from pydantic import BaseModel

class MaintenanceCategoryCreate(BaseModel):
    maintenance_category_name: str

class MaintenanceCategoryUpdate(BaseModel):
    maintenance_category_name: str | None = None

class MaintenanceCategoryResponse(BaseModel):
    id: int
    maintenance_category_name: str

    class Config:
        from_attributes = True