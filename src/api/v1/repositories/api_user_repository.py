from sqlalchemy.orm import Session
from src.api.v1.models.user_models.user_info import User
from src.api.v1.schemas import user_schemas as _US

async def assign_user_to_department(db: Session, user_id: int, department_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    
    user.department_id = department_id
    db.commit()
    db.refresh(user)
    return user
