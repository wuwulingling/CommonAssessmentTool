from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import Client
from app.clients.schema import ClientCreate, ClientUpdate
from typing import Dict, List

class ClientService:
    @staticmethod
    def create_client(db: Session, client: ClientCreate):
        # Check for existing client
        existing_client = db.query(Client).filter(Client.email == client.email).first()
        if existing_client:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        try:
            # Create new client
            db_client = Client(**client.dict())
            db.add(db_client)
            db.commit()
            db.refresh(db_client)
            return db_client
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create client"
            )

    @staticmethod
    def get_client(db: Session, client_id: int):
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        return client

    @staticmethod
    def get_clients(db: Session, skip: int = 0, limit: int = 100):
        try:
            clients = db.query(Client).offset(skip).limit(limit).all()
            total = db.query(Client).count()
            return {"clients": clients, "total": total}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve clients"
            )

    @staticmethod
    def update_client(db: Session, client_id: int, client_data: ClientUpdate):
        # Check if client exists
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        
        try:
            # Update only provided fields
            update_data = client_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(client, field, value)
            
            db.commit()
            db.refresh(client)
            return client
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update client"
            )

    @staticmethod
    def delete_client(db: Session, client_id: int):
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        
        try:
            db.delete(client)
            db.commit()
            
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete client"
            )
