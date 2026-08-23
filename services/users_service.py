from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from schemas.users import UserRegister, UserUpdate, TokenResponse
from fastapi.security import OAuth2PasswordRequestForm
from repositories import users_repository
from core.security import password_hash, create_access_token
from database.models import User
from sqlalchemy import select
from database.models import Role
def register_user(db: Session, newuser:UserRegister):
    exist_user = users_repository.get_user_by_email(db, newuser.email)
    if exist_user is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail = "Email is already registered")

    target_role_id = newuser.role_id
    if target_role_id is None:
        statement = select(Role).where(Role.id == 1)
        default_role = db.execute(statement).scalar_one_or_none()
        if default_role is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail = "Default Role is not configured")
        target_role_id = default_role.id
    
    hashed_pwd = password_hash.hash(newuser.hashed_password)
    user = User(
        name = newuser.name,
        email = newuser.email,
        hashed_password = hashed_pwd,
        dob = newuser.dob,
        personal_id = newuser.personal_id,
        address = newuser.address,
        blood_type = newuser.blood_type,
        role_id = target_role_id
    )

    return users_repository.register_user(db, user)

def get_user(db: Session, user_id: int):
    user = users_repository.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    return user

def get_all_users(db: Session):
    users = users_repository.get_all_users(db)
    return users

def update_user(db: Session, user_id: int, updateuser: UserUpdate):
    user = users_repository.get_user(db, user_id)

    if user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "User not found")

    if updateuser.name is not None:
        user.name = updateuser.name
    if updateuser.email is not None:
        user.email = updateuser.email
    if updateuser.dob is not None:
        user.dob = updateuser.dob
    if updateuser.personal_id is not None:
        user.personal_id = updateuser.personal_id
    if updateuser.address is not None:
        user.address = updateuser.address
    if updateuser.blood_type is not None:
        user.blood_type = updateuser.blood_type
    if updateuser.role_id is not None:
        user.role_id = updateuser.role_id

    return users_repository.update_user(db, user)

def delete_user(db:Session, user_id: int):
    user = users_repository.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User not found")

    return users_repository.delete_user(db, user)

def authenticate_user(db: Session, form_data: OAuth2PasswordRequestForm) -> TokenResponse:
    user = users_repository.get_user_by_email(db, form_data.username)
    
    if not user or not password_hash.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Email or Password"
        )

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(access_token=token, token_type="bearer")