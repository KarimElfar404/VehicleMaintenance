from fastapi import FastAPI
from database.database import engine, Base
import database.models

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Database connected successfully"}