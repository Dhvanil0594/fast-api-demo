from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database.database import get_db
from src.api.v1.schemas import schemas
from src.api.v1.models import models
from logger import logger
from src.api.v1.repositories.api_auth_repository import get_user_from_token
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/user")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user-auth/token")

@router.get("/me", response_model=schemas.UserResponse)
def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Get the logged-in user's data using the JWT token from the Authorization header.
    """
    logger.info("Inside function: get_user")

    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token is missing")
    
    # Log the entry of the function
    logger.info("Inside function: get_user")
    
    # Use the decoded token to retrieve user details
    user = get_user_from_token(token, db)
    
    return user
