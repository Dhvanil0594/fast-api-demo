from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional
from src.api.v1.schemas.department_schemas import DepartmentBase

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    department: Optional[DepartmentBase]

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    # Either username or email is optional, but at least one must be provided
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str

    # Root validator to ensure at least one of username or email is provided
    @model_validator(mode='before')
    def check_username_or_email(cls, values):
        if not values.get('username') and not values.get('email'):
            raise ValueError('Either username or email must be provided')
        return values

    class Config:
        str_min_length = 1
        str_strip_whitespace = True


class AssignUserToDepartmentRequest(BaseModel):
    user_id: int
    department_id: int