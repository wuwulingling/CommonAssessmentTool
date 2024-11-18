from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import HTMLResponse

from app.clients.service.logic import interpret_and_calculate
from app.clients.service.client_service import ClientService
from app.clients.schema import (
    PredictionInput,
    ClientCreate,
    ClientUpdate,
    Client as ClientSchema,
    ClientList
)

from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Client

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/predictions")
async def predict(data: PredictionInput):
    print("HERE")
    print(data.model_dump())
    return interpret_and_calculate(data.model_dump())



# CREATE
@router.post("/", response_model=ClientSchema, status_code=status.HTTP_201_CREATED)
async def create_client(
    client: ClientCreate,
    db: Session = Depends(get_db)
):
    return ClientService.create_client(db, client)

# READ - all clients
@router.get("/", response_model=ClientList)
async def read_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return ClientService.get_clients(db, skip, limit)

# READ - specific client
@router.get("/{client_id}", response_model=ClientSchema)
async def read_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    return ClientService.get_client(db, client_id)

# UPDATE
@router.put("/{client_id}", response_model=ClientSchema)
async def update_client(
    client_id: int,
    client_update: ClientUpdate,
    db: Session = Depends(get_db)
):
    return ClientService.update_client(db, client_id, client_update)

# DELETE
@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    ClientService.delete_client(db, client_id)
    return None
