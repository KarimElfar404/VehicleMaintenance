from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from schemas.users import UserResponse, UserRegister, UserUpdate, TokenResponse, UserLogin
from core.security import password_hash
from schemas.users import TokenResponse
from services import users_service
from fastapi import status
from typing import List
router = APIRouter()

@router.get("/user", response_model= List[UserResponse],  tags = ["Users"])
def get_all_users (db:Session = Depends(get_db)):
    return users_service.get_all_users(db)

@router.get("/user/{user_id}", response_model=UserResponse, tags = ["Users"])
def get_user (user_id: int, db:Session = Depends(get_db)):
    return users_service.get_user(db, user_id)

@router.post("/user", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags = ["Users"])
def register_user(newuser: UserRegister, db:Session = Depends(get_db)):
    return users_service.register_user(db, newuser)

@router.patch("/user/{user_id}",response_model=UserResponse, tags = ["Users"])
def update_user(user_id: int, updateuser: UserUpdate, db: Session = Depends(get_db)):
    return users_service.update_user(db, user_id, updateuser)

@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags = ["Users"])
def delete_user(user_id: int, db:Session = Depends(get_db)):
    users_service.delete_user(db, user_id)
    return None

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK, tags = ["Users"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return users_service.authenticate_user(db, form_data)