from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import Base, engine, SessionLocal
from app.db import models
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserResponse, UserLogin,Token
from app.core.security import hash_password, verify_password,create_access_token,get_current_user

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

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
    hashed_password = hash_password(user.password)
    new_user = models.User(email = user.email, password = hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# Create Login API
@app.post("/login", response_model = Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code = 400, detail = "Invalid Credentials")
    if not verify_password( form_data.password, db_user.password):
        raise HTTPException(status_code = 400, detail = "Invalid Credentials")

    # Create JWT token   
    access_token = create_access_token(data = {"sub": db_user.email})

    # Return token response
    print(f"Token: {access_token}")
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/profile")
def profile(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }
    
    