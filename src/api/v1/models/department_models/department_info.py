from database.database import Base
from sqlalchemy import Column, DateTime, Integer, String, text
from sqlalchemy.orm import relationship

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), index=True)
    created_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    created_by = Column(String(50)) 
    modified_at = Column(DateTime, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
    modified_by = Column(String(50)) 

    # One-to-many relationship with User
    users = relationship('User', back_populates='department')
