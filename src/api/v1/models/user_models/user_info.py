from sqlalchemy import Column, ForeignKey, Integer, String
from database.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True) 
    email = Column(String(100), unique=True, index=True)   
    hashed_password = Column(String(255))
    department_id = Column(Integer, ForeignKey('departments.id'))

    # Relationship to Department (Many-to-One)
    department = relationship('Department', back_populates='users')