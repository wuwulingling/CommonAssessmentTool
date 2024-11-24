"""
Pydantic models for data validation and serialization.
Defines schemas for client data, predictions, and API responses.
"""

# Standard library imports
from datetime import datetime
from typing import Optional, List

# Third-party imports
from pydantic import BaseModel, field_validator

class PredictionInput(BaseModel):
    """
    Schema for prediction input data containing all client assessment fields.
    Used for making predictions about client outcomes.
    """
    age: int
    gender: str
    work_experience: int
    canada_workex: int
    dep_num: int
    canada_born: str
    citizen_status: str
    level_of_schooling: str
    fluent_english: str
    reading_english_scale: int
    speaking_english_scale: int
    writing_english_scale: int
    numeracy_scale: int
    computer_scale: int
    transportation_bool: str
    caregiver_bool: str
    housing: str
    income_source: str
    felony_bool: str
    attending_school: str
    currently_employed: str
    substance_use: str
    time_unemployed: int
    need_mental_health_support_bool: str

class ClientBase(BaseModel):
    """
    Base schema for clients containing shared properties.
    Used as a base class for create, update, and response schemas.
    """
    name: str
    email: str
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    work_experience: Optional[int] = None
    canada_workex: Optional[int] = None
    dep_num: Optional[int] = None
    canada_born: Optional[str] = None
    citizen_status: Optional[str] = None
    level_of_schooling: Optional[str] = None
    # Case management specific fields
    case_status: Optional[str] = "new"
    case_type: Optional[str] = None
    assigned_to: Optional[str] = None
    priority: Optional[str] = "medium"
    case_notes: Optional[str] = None

    @field_validator('case_status')
    @classmethod
    def validate_case_status(cls, v):
        """Validate that case status is one of the allowed values."""
        allowed_statuses = ['new', 'in_progress', 'closed']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of {allowed_statuses}')
        return v

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        """Validate that priority is one of the allowed values."""
        allowed_priorities = ['low', 'medium', 'high']
        if v not in allowed_priorities:
            raise ValueError(f'Priority must be one of {allowed_priorities}')
        return v

class ClientCreate(ClientBase):
    """Schema for creating a new client. Inherits all fields from ClientBase."""
    pass

class ClientUpdate(ClientBase):
    """
    Schema for updating an existing client.
    Makes all fields optional to allow partial updates.
    """
    name: Optional[str] = None
    email: Optional[str] = None

class Client(ClientBase):
    """
    Schema for client responses, includes additional fields set by the system.
    Used for returning client data in API responses.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration for the Client model."""
        from_attributes = True

class ClientList(BaseModel):
    """
    Schema for returning multiple clients with pagination information.
    Used for list endpoints that return multiple clients.
    """
    clients: List[Client]
    total: int