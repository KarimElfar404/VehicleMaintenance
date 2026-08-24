from fastapi import FastAPI
from routers.users_router import router as UserRouter
from routers.roles_router import router as RoleRouter
from routers.drivers_router import router as DriverRouter
from routers.vehicle_router import router as VehicleRouter
from routers.maintenance_category_router import router as MaintenanceCategoryRouter
from routers.maintenance_subcategory_router import router as MaintenanceSubcategoryRouter
from routers.tickets_router import router as TicketRouter
from routers.maintenance_history_router import router as MaintenanceHistoryRouter
from database.database import engine, Base


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(UserRouter)
app.include_router(RoleRouter)
app.include_router(DriverRouter)
app.include_router(VehicleRouter)
app.include_router(MaintenanceCategoryRouter)
app.include_router(MaintenanceSubcategoryRouter)
app.include_router(TicketRouter)
app.include_router(MaintenanceHistoryRouter)
