"""
Repository for client data access operations.
Implements the repository pattern for client-related database operations.
Single Responsibility Principle (SRP): Create a separate repository layer for database operations, leaving higher-level business logic in the service class.
"""
from typing import Optional, Protocol, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status

from app.models import Client, ClientCase, User


class ClientRepositoryProtocol(Protocol):
    """Protocol defining the interface for client repositories"""
    
    def get_by_id(self, client_id: int) -> Optional[Client]: ...
    def get_all(self, skip: int, limit: int) -> Tuple[List[Client], int]: ...
    def filter_by_criteria(self, **criteria) -> List[Client]: ...
    def filter_by_services(self, **service_filters) -> List[Client]: ...
    def get_clients_by_success_rate(self, min_rate: int) -> List[Client]: ...
    def get_clients_by_case_worker(self, case_worker_id: int) -> List[Client]: ...
    def update(self, client_id: int, update_data: Dict[str, Any]) -> Client: ...
    def delete(self, client_id: int) -> None: ...


class ClientCaseRepositoryProtocol(Protocol):
    """Protocol defining the interface for client case repositories"""
    
    def get_by_client(self, client_id: int) -> List[ClientCase]: ...
    def get_by_client_and_user(self, client_id: int, user_id: int) -> Optional[ClientCase]: ...
    def create(self, client_id: int, user_id: int) -> ClientCase: ...
    def update(self, client_id: int, user_id: int, update_data: Dict[str, Any]) -> ClientCase: ...


class SQLAlchemyClientRepository:
    """SQLAlchemy implementation of the client repository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, client_id: int) -> Optional[Client]:
        """
        Get a client by ID
        
        Args:
            client_id: The client ID
            
        Returns:
            Optional[Client]: The client if found, None otherwise
        """
        client = self.db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )
        return client
    
    def get_all(self, skip: int, limit: int) -> Tuple[List[Client], int]:
        """
        Get all clients with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            Tuple[List[Client], int]: List of clients and total count
        """
        if skip < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Skip value cannot be negative"
            )
        if limit < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit must be greater than 0"
            )
        
        clients = self.db.query(Client).offset(skip).limit(limit).all()
        total = self.db.query(Client).count()
        return clients, total
    
    def filter_by_criteria(self, **criteria) -> List[Client]:
        """
        Filter clients by criteria

        Args:
            **criteria: Filter criteria as keyword arguments

        Returns:
            List[Client]: Filtered clients
        """
        query = self.db.query(Client)

    
        range_fields = {
            "age_min": ("age", ">="),
            "age_max": ("age", "<="),
            "time_unemployed": ("time_unemployed", "=="),
        }

        for field, value in criteria.items():
            if value is None:
                continue

            if field in range_fields:
                real_field, op = range_fields[field]
                column = getattr(Client, real_field)
                if op == ">=":
                    query = query.filter(column >= value)
                elif op == "<=":
                    query = query.filter(column <= value)
                elif op == "==":
                    query = query.filter(column == value)

            elif hasattr(Client, field):
                column = getattr(Client, field)
                query = query.filter(column == value)

            else:
                print(f"avoid unknown: {field}")

        try:
            return query.all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving clients: {str(e)}"
            )

    
    def filter_by_services(self, **service_filters) -> List[Client]:
        """
        Filter clients by service statuses
        
        Args:
            **service_filters: Service filters as keyword arguments
            
        Returns:
            List[Client]: Filtered clients
        """
        query = self.db.query(Client).join(ClientCase)
        
        for service_name, status in service_filters.items():
            if status is not None:
                filter_criteria = getattr(ClientCase, service_name) == status
                query = query.filter(filter_criteria)
        
        try:
            return query.all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error retrieving clients: {str(e)}"
            )
    
    def get_clients_by_success_rate(self, min_rate: int) -> List[Client]:
        """
        Get clients with success rate at or above the specified percentage
        
        Args:
            min_rate: Minimum success rate percentage
            
        Returns:
            List[Client]: Filtered clients
        """
        if not (0 <= min_rate <= 100):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Success rate must be between 0 and 100"
            )
        
        return self.db.query(Client).join(ClientCase).filter(
            ClientCase.success_rate >= min_rate
        ).all()
    
    def get_clients_by_case_worker(self, case_worker_id: int) -> List[Client]:
        """
        Get all clients assigned to a specific case worker
        
        Args:
            case_worker_id: The case worker ID
            
        Returns:
            List[Client]: Filtered clients
        """
        case_worker = self.db.query(User).filter(User.id == case_worker_id).first()
        if not case_worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case worker with id {case_worker_id} not found"
            )
        
        return self.db.query(Client).join(ClientCase).filter(
            ClientCase.user_id == case_worker_id
        ).all()
    
    def update(self, client_id: int, update_data: Dict[str, Any]) -> Client:
        """
        Update a client
        
        Args:
            client_id: The client ID
            update_data: The update data
            
        Returns:
            Client: The updated client
        """
        client = self.db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )
        
        for field, value in update_data.items():
            setattr(client, field, value)
        
        try:
            self.db.commit()
            self.db.refresh(client)
            return client
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update client: {str(e)}"
            )
    
    def delete(self, client_id: int) -> None:
        """
        Delete a client
        
        Args:
            client_id: The client ID
        """
        client = self.db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )
        
        try:
            # Delete associated client_cases
            self.db.query(ClientCase).filter(
                ClientCase.client_id == client_id
            ).delete()
            
            # Delete the client
            self.db.delete(client)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete client: {str(e)}"
            )


class SQLAlchemyClientCaseRepository:
    """SQLAlchemy implementation of the client case repository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_client(self, client_id: int) -> List[ClientCase]:
        """
        Get all cases for a client
        
        Args:
            client_id: The client ID
            
        Returns:
            List[ClientCase]: The client cases
        """
        client_cases = self.db.query(ClientCase).filter(ClientCase.client_id == client_id).all()
        if not client_cases:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No services found for client with id {client_id}"
            )
        return client_cases
    
    def get_by_client_and_user(self, client_id: int, user_id: int) -> Optional[ClientCase]:
        """
        Get a case by client and user
        
        Args:
            client_id: The client ID
            user_id: The user ID
            
        Returns:
            Optional[ClientCase]: The client case if found, None otherwise
        """
        return self.db.query(ClientCase).filter(
            ClientCase.client_id == client_id,
            ClientCase.user_id == user_id
        ).first()
    
    def create(self, client_id: int, user_id: int) -> ClientCase:
        """
        Create a new case assignment
        
        Args:
            client_id: The client ID
            user_id: The user ID
            
        Returns:
            ClientCase: The created client case
        """
        # Check if client exists
        client = self.db.query(Client).filter(Client.id == client_id).first()
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Client with id {client_id} not found"
            )
        
        # Check if case worker exists
        case_worker = self.db.query(User).filter(User.id == user_id).first()
        if not case_worker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Case worker with id {user_id} not found"
            )
        
        # Check if assignment already exists
        existing_case = self.get_by_client_and_user(client_id, user_id)
        if existing_case:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Client {client_id} already has a case assigned to case worker {user_id}"
            )
        
        try:
            # Create new case assignment with default service values
            new_case = ClientCase(
                client_id=client_id,
                user_id=user_id,
                employment_assistance=False,
                life_stabilization=False,
                retention_services=False,
                specialized_services=False,
                employment_related_financial_supports=False,
                employer_financial_supports=False,
                enhanced_referrals=False,
                success_rate=0
            )
            self.db.add(new_case)
            self.db.commit()
            self.db.refresh(new_case)
            return new_case
        
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create case assignment: {str(e)}"
            )
    
    def update(self, client_id: int, user_id: int, update_data: Dict[str, Any]) -> ClientCase:
        """
        Update a client case
        
        Args:
            client_id: The client ID
            user_id: The user ID
            update_data: The update data
            
        Returns:
            ClientCase: The updated client case
        """
        client_case = self.get_by_client_and_user(client_id, user_id)
        if not client_case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No case found for client {client_id} with case worker {user_id}. "
                    f"Cannot update services for a non-existent case assignment."
            )
        
        for field, value in update_data.items():
            setattr(client_case, field, value)
        
        try:
            self.db.commit()
            self.db.refresh(client_case)
            return client_case
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update client services: {str(e)}"
            )