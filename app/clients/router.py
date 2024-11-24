"""
Router module for client-related endpoints.
Handles all HTTP requests for client operations including create, read, update, and delete.
"""

# Standard library imports
#from typing import List

# Third-party imports
from fastapi import APIRouter, Depends, status
#from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

# Local application imports
from app.database import get_db
#from app.models import Client
from app.clients.schema import (
    PredictionInput,
    ClientCreate,
    ClientUpdate,
    Client as ClientSchema,
    ClientList
)
from app.clients.service.logic import interpret_and_calculate
from app.clients.service.client_service import ClientService

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/predictions")
async def predict(data: PredictionInput):
    """
    Make predictions based on input data.

    Args:
        data: Input data for prediction

    Returns:
        dict: Calculated predictions
    """
    print("HERE")
    print(data.model_dump())
    return interpret_and_calculate(data.model_dump())

@router.post("/", response_model=ClientSchema, status_code=status.HTTP_201_CREATED)
async def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new client.

    Args:
        client: Client data for creation
        db: Database session dependency

    Returns:
        ClientSchema: Created client data
    """
    return ClientService.create_client(db, client)

@router.get("/", response_model=ClientList)
async def read_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Retrieve all clients with pagination.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session dependency

    Returns:
        ClientList: List of clients
    """
    return ClientService.get_clients(db, skip, limit)

@router.get("/{client_id}", response_model=ClientSchema)
async def read_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific client by ID.

    Args:
        client_id: ID of the client to retrieve
        db: Database session dependency

    Returns:
        ClientSchema: Retrieved client data
    """
    return ClientService.get_client(db, client_id)

@router.put("/{client_id}", response_model=ClientSchema)
async def update_client(
    client_id: int,
    client_update: ClientUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a specific client.

    Args:
        client_id: ID of the client to update
        client_update: Updated client data
        db: Database session dependency

    Returns:
        ClientSchema: Updated client data
    """
    return ClientService.update_client(db, client_id, client_update)

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a specific client.

    Args:
        client_id: ID of the client to delete
        db: Database session dependency

    Returns:
        None
    """
    ClientService.delete_client(db, client_id)
    return None
