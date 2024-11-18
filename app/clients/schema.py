from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime

class PredictionInput(BaseModel):
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

# Base schema for clients (shared properties)
class ClientBase(BaseModel):
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

    # Validators for data consistency
    @field_validator('case_status')
    @classmethod
    def validate_case_status(cls, v):
        allowed_statuses = ['new', 'in_progress', 'closed']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of {allowed_statuses}')
        return v

    @field_validator('priority')
    @classmethod
    def validate_priority(cls, v):
        allowed_priorities = ['low', 'medium', 'high']
        if v not in allowed_priorities:
            raise ValueError(f'Priority must be one of {allowed_priorities}')
        return v

# Schema for creating a new client
class ClientCreate(ClientBase):
    pass

# Schema for updating a client
class ClientUpdate(ClientBase):
    # All fields are optional for updates
    name: Optional[str] = None
    email: Optional[str] = None

# Schema for returning client data
class Client(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        # This tells Pydantic to convert even non-dict obj to json
        from_attributes = True

# Schema for returning multiple clients
class ClientList(BaseModel):
    clients: list[Client]
    total: int
