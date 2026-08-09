from fastapi import FastAPI
from routers.users_router import router as UserRouter
from routers.roles_router import router as RoleRouter
from routers.drivers_router import router as DriverRouter
from routers.vehicle_router import router as VehicleRouter
from database.database import engine, Base


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(UserRouter)
app.include_router(RoleRouter)
app.include_router(DriverRouter)
app.include_router(VehicleRouter)
