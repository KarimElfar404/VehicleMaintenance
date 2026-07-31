from database.models import User
from database.database import get_db
from sqlalchemy.orm import Session
from schemas.users import UserUpdate, UserResponse, UserRegister
from sqlalchemy import select
from fastapi import HTTPException, status
from core.security import password_hash

def get_user(db: Session, user_id: int):
    return db.get(User, user_id)

def get_all_users(db: Session):
    statement = select(User)
    return db.execute(statement).scalars().all()

def get_user_by_email(db: Session, email: str):
    statement = (
        select(User)
        .where(User.email == email)
    )
    return db.scalar(statement)

def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()

def register_user(db: Session, newuser: User):

    db.add(newuser)
    db.commit()
    db.refresh(newuser)
    return newuser


def update_user(db: Session, user: User):

    db.commit()
    db.refresh(user)
    return user