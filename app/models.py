"""
Database models module defining SQLAlchemy ORM models for the Common Assessment Tool.
Contains the Client model for storing client information in the database.
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base

class Client(Base):
    """
    Client model representing client data in the database.
    """
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
    
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self):
        """Return string representation of the Client object."""
        return f"Client(id={self.id}, name={self.name}, age={self.age})"