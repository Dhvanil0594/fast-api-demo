from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from jose import jwt
from src.api.v1.models.user_models.user_info import User
from sqlalchemy.orm import Session
from config.config import settings
from logger import logger

async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        logger.info(f"Token verified successfully......{payload}")
        return payload
    except:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

async def get_user_from_token(token: str, db: Session) -> User:
    """
    Decodes the JWT token and retrieves the user from the database.
    """
    try:
        # Decode the token to get the payload
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])  
        logger.info(f"Decoded token: {payload}")
        user_email = payload.get("sub")  # The subject is the user ID (or email)
        
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token or missing user ID")
        
        # Query the database for the user
        user = db.query(User).filter(User.email == user_email).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    except Exception as e:
        logger.error(f"Error decoding token: {e}")
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    