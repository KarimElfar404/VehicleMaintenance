from fastapi import FastAPI
from routers.users_router import router as UserRouter
from database.database import engine, Base
import database.models

Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(UserRouter)
