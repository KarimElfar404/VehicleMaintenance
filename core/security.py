from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from core.config import settings
from fastapi import Depends
from sqlalchemy.orm import Session, joinedload
from database.database import get_db
from database.models import User
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone


password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        settings.algorithm,
    )
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            settings.algorithm,
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "User Not Found")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "User Not Found")

    user = (
        db.query(User)
        .options(
            joinedload(User.driver_profile),
            joinedload(User.role)
        )
        .filter(User.id == int(user_id))
        .first( )
    )
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Invalid Authentication state")

    return user