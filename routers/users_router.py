from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from schemas.users import UserResponse, UserRegister, UserUpdate, TokenResponse, UserLogin
from core.security import password_hash
from schemas.users import TokenResponse
from services import users_service
from core.security import get_current_user
from fastapi import status
from typing import List
from database.models import User
from role_permissions import require_permission
router = APIRouter()

@router.get("/users", response_model= List[UserResponse],  tags = ["Users"])
def get_all_users (db:Session = Depends(get_db), current_user: User = Depends(require_permission("user:read"))):
    return users_service.get_all_users(db)

@router.get("/users/{user_id}", response_model=UserResponse, tags = ["Users"])
def get_user (user_id: int, db:Session = Depends(get_db), current_user: User = Depends(require_permission("user:read"))):
    return users_service.get_user(db, user_id)

@router.get("/users/{user_id}", response_model=UserResponse, tags = ["Users"])
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("user:read"))
):
    return users_service.get_user_by_id(db, user_id=user_id, current_user=current_user)

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags = ["Users"])
def register_user(newuser: UserRegister, db:Session = Depends(get_db)):
    return users_service.register_user(db, newuser)

@router.patch("/users/{user_id}",response_model=UserResponse, tags = ["Users"])
def update_user(user_id: int, updateuser: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_permission("user:update"))):
    return users_service.update_user(db, user_id, updateuser)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags = ["Users"])
def delete_user(user_id: int, db:Session = Depends(get_db), current_user: User = Depends(require_permission("user:delete"))):
    users_service.delete_user(db, user_id)
    return None

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK, tags = ["Users"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return users_service.authenticate_user(db, form_data)