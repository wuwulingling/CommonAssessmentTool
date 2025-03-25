# app/clients/service/client_service.py
"""
Client service for client-related business logic.
Encapsulates business rules and coordinates with repositories.
"""
from typing import Dict, Any, List, Optional, Tuple

from app.models import Client, ClientCase
from app.clients.repository import ClientRepositoryProtocol, ClientCaseRepositoryProtocol
from app.clients.schema import ClientUpdate, ServiceUpdate


class ClientService:
    """Service for client-related operations"""
    
    def __init__(
        self, 
        client_repository: ClientRepositoryProtocol,
        client_case_repository: ClientCaseRepositoryProtocol
    ):
        """
        Initialize with repositories
        
        Args:
            client_repository: Client repository
            client_case_repository: Client case repository
        """
        self.client_repository = client_repository
        self.client_case_repository = client_case_repository
    
    def get_client(self, client_id: int) -> Client:
        """
        Get a client by ID
        
        Args:
            client_id: The client ID
            
        Returns:
            Client: The client
        """
        return self.client_repository.get_by_id(client_id)
    
    def get_clients(self, skip: int = 0, limit: int = 50) -> Dict[str, Any]:
        """
        Get clients with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records
            
        Returns:
            Dict[str, Any]: Clients and total count
        """
        clients, total = self.client_repository.get_all(skip, limit)
        return {"clients": clients, "total": total}
    
    def get_clients_by_criteria(self, **criteria) -> List[Client]:
        """
        Get clients by criteria
        
        Args:
            **criteria: Filter criteria
            
        Returns:
            List[Client]: Filtered clients
        """
        return self.client_repository.filter_by_criteria(**criteria)
    
    def get_clients_by_services(self, **service_filters) -> List[Client]:
        """
        Get clients by service filters
        
        Args:
            **service_filters: Service filters
            
        Returns:
            List[Client]: Filtered clients
        """
        return self.client_repository.filter_by_services(**service_filters)
    
    def get_client_services(self, client_id: int) -> List[ClientCase]:
        """
        Get services for a client
        
        Args:
            client_id: The client ID
            
        Returns:
            List[ClientCase]: Client services
        """
        return self.client_case_repository.get_by_client(client_id)
    
    def get_clients_by_success_rate(self, min_rate: int = 70) -> List[Client]:
        """
        Get clients by success rate
        
        Args:
            min_rate: Minimum success rate
            
        Returns:
            List[Client]: Filtered clients
        """
        return self.client_repository.get_clients_by_success_rate(min_rate)
    
    def get_clients_by_case_worker(self, case_worker_id: int) -> List[Client]:
        """
        Get clients by case worker
        
        Args:
            case_worker_id: The case worker ID
            
        Returns:
            List[Client]: Filtered clients
        """
        return self.client_repository.get_clients_by_case_worker(case_worker_id)
    
    def update_client(self, client_id: int, client_update: ClientUpdate) -> Client:
        """
        Update a client
        
        Args:
            client_id: The client ID
            client_update: The update data
            
        Returns:
            Client: The updated client
        """
        update_data = client_update.dict(exclude_unset=True)
        return self.client_repository.update(client_id, update_data)
    
    def update_client_services(
        self, 
        client_id: int,
        user_id: int,
        service_update: ServiceUpdate
    ) -> ClientCase:
        """
        Update client services
        
        Args:
            client_id: The client ID
            user_id: The user ID
            service_update: The service update data
            
        Returns:
            ClientCase: The updated client case
        """
        update_data = service_update.dict(exclude_unset=True)
        return self.client_case_repository.update(client_id, user_id, update_data)
    
    def create_case_assignment(
        self, 
        client_id: int,
        case_worker_id: int
    ) -> ClientCase:
        """
        Create a case assignment
        
        Args:
            client_id: The client ID
            case_worker_id: The case worker ID
            
        Returns:
            ClientCase: The created client case
        """
        return self.client_case_repository.create(client_id, case_worker_id)
    
    def delete_client(self, client_id: int) -> None:
        """
        Delete a client
        
        Args:
            client_id: The client ID
        """
        self.client_repository.delete(client_id)