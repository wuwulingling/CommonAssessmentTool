"""
Client service module handling all database operations for clients.
Provides CRUD operations and business logic for client management.
"""

# Third-party imports
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

# Local application imports
from app.models import Client
from app.clients.schema import ClientCreate, ClientUpdate

class ClientService:
    """
    Service class handling all client-related database operations.
    Implements CRUD operations with proper error handling and validation.
    """

    @staticmethod
    def create_client(db: Session, client: ClientCreate):
        """
        Create a new client in the database.

        Args:
            db: Database session
            client: Client data for creation

        Returns:
            Client: Created client instance

        Raises:
            HTTPException: If email already exists or creation fails
        """
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
        except Exception as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create client"
            ) from exc

    @staticmethod
    def get_client(db: Session, client_id: int):
        """
        Retrieve a specific client by ID.

        Args:
            db: Database session
            client_id: ID of the client to retrieve

        Returns:
            Client: Retrieved client instance

        Raises:
            HTTPException: If client is not found
        """
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        return client

    @staticmethod
    def get_clients(db: Session, skip: int = 0, limit: int = 100):
        """
        Retrieve multiple clients with pagination.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            dict: Dictionary containing clients list and total count

        Raises:
            HTTPException: If retrieval fails
        """
        try:
            clients = db.query(Client).offset(skip).limit(limit).all()
            total = db.query(Client).count()
            return {"clients": clients, "total": total}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve clients"
            ) from exc

    @staticmethod
    def update_client(db: Session, client_id: int, client_data: ClientUpdate):
        """
        Update an existing client's information.

        Args:
            db: Database session
            client_id: ID of the client to update
            client_data: New client data

        Returns:
            Client: Updated client instance

        Raises:
            HTTPException: If client is not found or update fails
        """
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )

        try:
            update_data = client_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(client, field, value)
            db.commit()
            db.refresh(client)
            return client
        except Exception as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update client"
            ) from exc

    @staticmethod
    def delete_client(db: Session, client_id: int):
        """
        Delete a client from the database.

        Args:
            db: Database session
            client_id: ID of the client to delete

        Raises:
            HTTPException: If client is not found or deletion fails
        """
        client = db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )

        try:
            db.delete(client)
            db.commit()
        except Exception as exc:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete client"
            ) from exc