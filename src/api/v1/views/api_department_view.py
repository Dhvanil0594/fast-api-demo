from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database.database import get_db
from src.api.v1.schemas import department_schemas as _DS
from logger import logger
from src.api.v1.repositories import api_department_repository as _DR

router = APIRouter(prefix="/department")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user-auth/token")


@router.post("/", response_model=_DS.Department)
def create_department(
    department: _DS.DepartmentCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme),
):
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token is missing")
    
    return _DR.create_department(db=db, department=department, token=token)

@router.get("/", response_model=list[_DS.Department] | _DS.Department)
def read_departments(
    department_id: int = None,  # Optional query parameter
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token is missing")

    if department_id is not None:
        # If department_id is provided, return a specific department
        db_department = _DR.get_department_by_id(db, department_id=department_id)
        if db_department is None:
            raise HTTPException(status_code=404, detail="Department not found")
        return db_department

    # If department_id is not provided, return a list of departments
    return _DR.get_departments(db=db, skip=skip, limit=limit)

@router.put("/{department_id}", response_model=_DS.Department)
def update_department(
    department_id: int,
    department_data: _DS.DepartmentUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token is missing")

    db_department = _DR.update_department(db, department_id, department_data, token)
    if not db_department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    
    return db_department

@router.delete("/{department_id}", status_code=status.HTTP_200_OK)
def delete_department(department_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):

    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization token is missing")

    # Check if the department exists and delete it
    is_deleted = _DR.delete_department(db, department_id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Department not found")

    return {"message": "Department deleted successfully"}