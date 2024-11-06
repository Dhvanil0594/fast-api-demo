from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from database.database import get_db
from src.api.v1.schemas import user_schemas as _US
from src.api.v1.models.user_models import user_info as _UI
from logger import logger
from src.api.v1.repositories.api_auth_repository import get_user_from_token, verify_token
from fastapi.security import OAuth2PasswordBearer
from src.api.v1.repositories import api_department_repository as _DR
from src.api.v1.repositories import api_user_repository as _UR

router = APIRouter(prefix="/user")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user-auth/token")

@router.get("/me", response_model=_US.UserResponse)
async def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Get the logged-in user's data using the JWT token from the Authorization header.
    """
    logger.info("Inside function: get_user")

    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token is missing")
    
    # Log the entry of the function
    logger.info("Inside function: get_user")
    
    # Use the decoded token to retrieve user details
    user = await get_user_from_token(token, db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Ensure the department relationship is loaded
    if user.department:
        user.department  # This will trigger lazy loading if it's not already loaded

    return user


@router.post("/assign-user-to-department", response_model=_US.UserResponse, status_code=status.HTTP_200_OK)
async def assign_user_to_department(
    request: _US.AssignUserToDepartmentRequest, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token is missing")
    
    check_token = verify_token(token)
    # Check if the department exists
    department = await _DR.get_department_by_id(db, request.department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")

    # Assign the user to the department
    user = await _UR.assign_user_to_department(db, request.user_id, request.department_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user