from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class DepartmentBase(BaseModel):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str]
    # modified_by: Optional[str]

class Department(DepartmentBase):
    id: int
    created_at: datetime
    created_by: Optional[str]
    modified_at: datetime
    modified_by: Optional[str]
    users: list['User'] = [] 

    class Config:
        from_attributes = True

class User(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True