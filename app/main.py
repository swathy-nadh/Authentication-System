from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.db.database import Base, engine, SessionLocal
from app.db import models
from app.schemas.user import UserCreate, UserResponse, UserLogin

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Password hashing setup
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create User API
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    #Check duplicate email
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code = 400, detail = "Email already registered")
    
    #hash password
    hashed_password = pwd_context.hash(user.password)
    new_user = models.User(
        email = user.email,
        password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print(f"password:  {hashed_password}")
    return new_user

# Create Login API
@app.post("/login", response_model = UserResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code = 400, detail = "Invalid Credentials")
    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(status_code = 400, detail = "Invalid Credentials")
    
    return db_user