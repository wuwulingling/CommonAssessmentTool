from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String(100), unique=True, index=True) 
    phone = Column(String(20))
    age = Column(Integer)
    gender = Column(String)
    work_experience = Column(Integer)
    canada_workex = Column(Integer)
    dep_num = Column(Integer)
    canada_born = Column(String(3))
    citizen_status = Column(String(50))
    level_of_schooling = Column(String(100))

    case_status = Column(String(50), default="new")
    case_type = Column(String(100))  
    assigned_to = Column(String(100))  
    priority = Column(String(20))
    case_notes = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
