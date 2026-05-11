from passlib.context import CryptContext
from jose import jwt,JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db import models
from app.db.database import SessionLocal
from datetime import datetime, timedelta
from app.core.config import (SECRET_KEY, ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES)

# Password hashing setup
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

#hash password
def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")
def create_access_token(data: dict):

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm = ALGORITHM)

    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code = 401, detail = "Couldn't validate credentials")
    try:
        payload = jwt.decode(token,
            SECRET_KEY,
            algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:

        raise credentials_exception

    db = SessionLocal()

    user = db.query(models.User).filter(
        models.User.email == email
    ).first()

    db.close()

    if user is None:
        raise credentials_exception

    return user
     