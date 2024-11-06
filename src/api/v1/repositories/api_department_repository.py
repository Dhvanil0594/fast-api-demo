from datetime import datetime, timezone
from pytz import utc
from sqlalchemy.orm import Session
from src.api.v1.models.department_models.department_info import Department
from src.api.v1.schemas.department_schemas import DepartmentCreate, DepartmentUpdate
from src.api.v1.repositories.api_auth_repository import get_user_from_token
from logger import logger

def get_departments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Department).order_by(Department.created_at.desc()).offset(skip).limit(limit).all()

def get_department_by_id(db: Session, department_id: int):
    return db.query(Department).filter(Department.id == department_id).first()

def create_department(db: Session, department: DepartmentCreate, token: str):
    user = get_user_from_token(token, db)
    # Create a new department
    db_department = Department(name=department.name, created_by=user.id, modified_by=user.id)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


def update_department(db: Session, department_id: int, department_data: DepartmentUpdate, token: str):
    user = get_user_from_token(token, db)
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if not db_department:
        return None
    
    if department_data.name:
        db_department.name = department_data.name
        db_department.modified_by = user.id
        db_department.modified_at = datetime.now()

    db.commit()
    db.refresh(db_department)
    return db_department

def delete_department(db: Session, department_id: int):
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if db_department:
        db.delete(db_department)
        db.commit()
        return True
    return False