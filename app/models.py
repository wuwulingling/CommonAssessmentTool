"""
Database models module defining SQLAlchemy ORM models for the Common Assessment Tool.
Contains the Client model for storing client information in the database.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, text
from sqlalchemy.sql import func
from app.database import Base

class Client(Base):
    """
    Client model representing client data in the database.
    
    Attributes:
        id (int): Primary key
        name (str): Client's name
        email (str): Client's email address
        phone (str): Client's phone number
        age (int): Client's age
        gender (str): Client's gender
        work_experience (int): Years of work experience
        canada_workex (int): Years of work experience in Canada
        dep_num (int): Number of dependents
        canada_born (str): Born in Canada indicator
        citizen_status (str): Citizenship status
        level_of_schooling (str): Education level
        case_status (str): Current case status
        case_type (str): Type of case
        assigned_to (str): Case manager assigned
        priority (str): Case priority level
        case_notes (Text): Additional case notes
        created_at (DateTime): Record creation timestamp
        updated_at (DateTime): Record last update timestamp
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
    created_at = Column(
        DateTime,
        server_default=text('CURRENT_TIMESTAMP'),
        nullable=False
    )
    updated_at = Column(
        DateTime,
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=text('CURRENT_TIMESTAMP'),
        nullable=False
    )

    def __repr__(self):
        """Return string representation of the Client object."""
        return f"Client(id={self.id}, name={self.name}, age={self.age})"

    def __str__(self):
        """Return human-readable string representation of the Client object."""
        return f"Client {self.name} (ID: {self.id})"

    def to_dict(self):
        """Convert Client object to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'age': self.age,
            'gender': self.gender,
            'work_experience': self.work_experience,
            'canada_workex': self.canada_workex,
            'dep_num': self.dep_num,
            'canada_born': self.canada_born,
            'citizen_status': self.citizen_status,
            'level_of_schooling': self.level_of_schooling,
            'case_status': self.case_status,
            'case_type': self.case_type,
            'assigned_to': self.assigned_to,
            'priority': self.priority,
            'case_notes': self.case_notes,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        