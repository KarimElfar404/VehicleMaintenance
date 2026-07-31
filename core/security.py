from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from core.config import settings
from fastapi import Depends
from sqlalchemy.orm import Session
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
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes = 30))
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

    user = db.get(User, int(user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "User Not Found")

    return user