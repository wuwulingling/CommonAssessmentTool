"""
Router for client endpoints.
Handles HTTP requests for client-related operations.
"""

from fastapi import HTTPException
from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional
from app.auth.dependencies import get_current_user, get_admin_user
from app.models import User, UserRole

from app.auth.dependencies import get_current_user, get_admin_user
from app.models import User
from app.clients.dependencies import get_client_service
from app.clients.schema import (
    ClientResponse,
    ClientUpdate,
    ClientListResponse,
    ServiceResponse,
    ServiceUpdate,
    PredictionInput,
)
from app.clients.service.logic import interpret_and_calculate

# Add the Code to see the Prediction API and Test It per Piazza Post
from app.clients.service.logic import interpret_and_calculate
from app.clients.schema import PredictionInput

# Add the Code to see the Prediction API and Test It per Piazza Post
from app.clients.service.logic import interpret_and_calculate
from app.clients.schema import PredictionInput

router = APIRouter(tags=["clients"])


@router.post("/predictions")
async def predict(data: PredictionInput):
    print("HERE")
    print(data.model_dump())
    return interpret_and_calculate(data.model_dump())


# Import the model_manager functions for switching models, getting the current model, and listing all available models
from app.clients.service.model_manager import list_models, get_current_model_name, switch_model

model_router = APIRouter(prefix="/models", tags=["models"])


# API Endpoint for listing all available models
@model_router.get("/", response_model=list)
def get_available_models():
    return list_models()


# API Endpoint for getting the name of the currently active model
@model_router.get("/current", response_model=str)
def get_active_model():
    return get_current_model_name()


# API Endpoint for switching to a different model by name
@model_router.post("/switch/{model_name}")
def change_model(model_name: str):
    try:
        switch_model(model_name)
        return {"message": f"Switched to model: {model_name}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=ClientListResponse)
async def get_clients(
    client_service=Depends(get_client_service),
    current_user: User = Depends(get_admin_user),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=50, ge=1, le=150, description="Maximum number of records to return"),
):
    """
    Get all clients with pagination (admin only)

    Args:
        client_service: Client service
        current_user: Current admin user
        skip: Number of records to skip
        limit: Maximum number of records

    Returns:
        ClientListResponse: Clients and total count
    """
    return client_service.get_clients(skip, limit)


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    client_service=Depends(get_client_service),
    current_user: User = Depends(get_admin_user),
):
    """
    Get a specific client by ID (admin only)

    Args:
        client_id: The client ID
        client_service: Client service
        current_user: Current admin user

    Returns:
        ClientResponse: The client
    """
    return client_service.get_client(client_id)


@router.get("/search/by-criteria", response_model=List[ClientResponse])
async def get_clients_by_criteria(
    employment_status: Optional[bool] = None,
    education_level: Optional[int] = Query(None, ge=1, le=14),
    age_min: Optional[int] = Query(None, ge=18),
    gender: Optional[int] = Query(None, ge=1, le=2),
    work_experience: Optional[int] = Query(None, ge=0),
    canada_workex: Optional[int] = Query(None, ge=0),
    dep_num: Optional[int] = Query(None, ge=0),
    canada_born: Optional[bool] = None,
    citizen_status: Optional[bool] = None,
    fluent_english: Optional[bool] = None,
    reading_english_scale: Optional[int] = Query(None, ge=0, le=10),
    speaking_english_scale: Optional[int] = Query(None, ge=0, le=10),
    writing_english_scale: Optional[int] = Query(None, ge=0, le=10),
    numeracy_scale: Optional[int] = Query(None, ge=0, le=10),
    computer_scale: Optional[int] = Query(None, ge=0, le=10),
    transportation_bool: Optional[bool] = None,
    caregiver_bool: Optional[bool] = None,
    housing: Optional[int] = Query(None, ge=1, le=10),
    income_source: Optional[int] = Query(None, ge=1, le=11),
    felony_bool: Optional[bool] = None,
    attending_school: Optional[bool] = None,
    substance_use: Optional[bool] = None,
    time_unemployed: Optional[int] = Query(None, ge=0),
    need_mental_health_support_bool: Optional[bool] = None,
    client_service=Depends(get_client_service),
    current_user: User = Depends(get_admin_user),
):
    """
    Search clients by criteria (admin only)

    Args:
        Multiple filter criteria as query parameters
        client_service: Client service
        current_user: Current admin user

    Returns:
        List[ClientResponse]: Filtered clients
    """
    return client_service.get_clients_by_criteria(
        employment_status=employment_status,
        education_level=education_level,
        age_min=age_min,
        gender=gender,
        work_experience=work_experience,
        canada_workex=canada_workex,
        dep_num=dep_num,
        canada_born=canada_born,
        citizen_status=citizen_status,
        fluent_english=fluent_english,
        reading_english_scale=reading_english_scale,
        speaking_english_scale=speaking_english_scale,
        writing_english_scale=writing_english_scale,
        numeracy_scale=numeracy_scale,
        computer_scale=computer_scale,
        transportation_bool=transportation_bool,
        caregiver_bool=caregiver_bool,
        housing=housing,
        income_source=income_source,
        felony_bool=felony_bool,
        attending_school=attending_school,
        substance_use=substance_use,
        time_unemployed=time_unemployed,
        need_mental_health_support_bool=need_mental_health_support_bool,
    )


@router.get("/search/by-services", response_model=List[ClientResponse])
async def get_clients_by_services(
    employment_assistance: Optional[bool] = None,
    life_stabilization: Optional[bool] = None,
    retention_services: Optional[bool] = None,
    specialized_services: Optional[bool] = None,
    employment_related_financial_supports: Optional[bool] = None,
    employer_financial_supports: Optional[bool] = None,
    enhanced_referrals: Optional[bool] = None,
    client_service=Depends(get_client_service),
    current_user: User = Depends(get_admin_user),
):
    """
    Get clients filtered by service statuses (admin only)

    Args:
        Multiple service filters as query parameters
        client_service: Client service
        current_user: Current admin user

    Returns:
        List[ClientResponse]: Filtered clients
    """
    return client_service.get_clients_by_services(
        employment_assistance=employment_assistance,
        life_stabilization=life_stabilization,
        retention_services=retention_services,
        specialized_services=specialized_services,
        employment_related_financial_supports=employment_related_financial_supports,
        employer_financial_supports=employer_financial_supports,
        enhanced_referrals=enhanced_referrals,
    )


@router.get("/{client_id}/services", response_model=List[ServiceResponse])
async def get_client_services(
    client_id: int,
    client_service=Depends(get_client_service),
    current_user: User = Depends(get_admin_user),
):
    """
    Get all services for a specific client (admin only)

    Args:
        client_id: The client ID
        client_service: Client service
        current_user: Current admin user

    Returns:
        List[ServiceResponse]: Client services
    """
    return client_service.get_client_services(client_id)


@router.get("/search/success-rate", response_model=List[ClientResponse])
async def get_clients_by_success_rate(
    min_rate: int = Query(70, ge=0, le=100, description="Minimum success rate percentage"),
    client_service=Depends(get_client_service),
    current_user: User = Depends(get_admin_user),
):
    """
    Get clients with success rate above threshold (admin only)

    Args:
        min_rate: Minimum success rate
        client_service: Client service
        current_user: Current admin user

    Returns:
        List[ClientResponse]: Filtered clients
    """
    return client_service.get_clients_by_success_rate(min_rate)


@router.get("/case-worker/{case_worker_id}", response_model=List[ClientResponse])
async def get_clients_by_case_worker(
    case_worker_id: int,
    client_service=Depends(get_client_service),
    current_user: User = Depends(get_current_user),
):
    """
    Get clients by case worker

    Args:
        case_worker_id: The case worker ID
        client_service: Client service
        current_user: Current user

    Returns:
        List[ClientResponse]: Filtered clients
    """
    return client_service.get_clients_by_case_worker(case_worker_id)


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    client_service=Depends(get_client_service),
    current_user: User = Depends(get_admin_user),
):
    """
    Update a client (admin only)

    Args:
        client_id: The client ID
        client_data: Client update data
        client_service: Client service
        current_user: Current admin user

    Returns:
        ClientResponse: Updated client
    """
    return client_service.update_client(client_id, client_data)


@router.put("/{client_id}/services/{user_id}", response_model=ServiceResponse)
async def update_client_services(
    client_id: int,
    user_id: int,
    service_update: ServiceUpdate,
    client_service=Depends(get_client_service),
    current_user: User = Depends(get_current_user),
):
    """
    Update client services

    Args:
        client_id: The client ID
        user_id: The user ID
        service_update: Service update data
        client_service: Client service
        current_user: Current user

    Returns:
        ServiceResponse: Updated service
    """
    return client_service.update_client_services(client_id, user_id, service_update)


@router.post("/{client_id}/case-assignment", response_model=ServiceResponse)
async def create_case_assignment(
    client_id: int,
    case_worker_id: int = Query(..., description="Case worker ID to assign"),
    client_service=Depends(get_client_service),
    current_user: User = Depends(get_admin_user),
):
    """
    Create a new case assignment (admin only)

    Args:
        client_id: The client ID
        case_worker_id: The case worker ID
        client_service: Client service
        current_user: Current admin user

    Returns:
        ServiceResponse: Created case assignment
    """
    return client_service.create_case_assignment(client_id, case_worker_id)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
    client_service=Depends(get_client_service),
    current_user: User = Depends(get_admin_user),
):
    """
    Delete a client (admin only)

    Args:
        client_id: The client ID
        client_service: Client service
        current_user: Current admin user
    """
    client_service.delete_client(client_id)
    return None


@router.get(
    "/test-new-endpoint",
    tags=["test-tag"],
    summary="Brief description",
    description="Detailed description",
    response_description="Description of the response",
)
async def new_endpoint():
    """
    This docstring will appear in the Swagger documentation

    Returns:
        dict: Description of what the endpoint returns
    """
    return {"message": "Hello World"}
