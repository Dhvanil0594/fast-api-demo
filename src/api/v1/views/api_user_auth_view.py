from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.api.v1.models import models
from src.api.v1.schemas import schemas
from src.api.v1.services import utils
from database.database import get_db
from config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from src.api.v1.repositories.api_auth_repository import create_access_token
from logger import logger

router = APIRouter(prefix="/user-auth")

@router.post("/signup", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_password = utils.hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Inside function: login. user: {user}")

    # Check if the user exists using username or email
    db_user = None
    if user.email:
        db_user = db.query(models.User).filter(models.User.email == user.email).first()
    elif user.username:
        db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user or not utils.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Create an access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}