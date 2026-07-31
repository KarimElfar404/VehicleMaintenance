from fastapi import FastAPI
from routers.users_router import router as UserRouter
from routers.roles_router import router as RoleRouter
from database.database import engine, Base


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(UserRouter)
app.include_router(RoleRouter)