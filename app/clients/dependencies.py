"""
Client dependencies for FastAPI dependency injection.
Provides injectable dependencies for repositories and services.
"""
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.clients.repository import SQLAlchemyClientRepository, SQLAlchemyClientCaseRepository
from app.clients.service.client_service import ClientService


def get_client_repository(db: Session = Depends(get_db)):
    """
    Get client repository
    
    Args:
        db: Database session
        
    Returns:
        SQLAlchemyClientRepository: Client repository
    """
    return SQLAlchemyClientRepository(db)


def get_client_case_repository(db: Session = Depends(get_db)):
    """
    Get client case repository
    
    Args:
        db: Database session
        
    Returns:
        SQLAlchemyClientCaseRepository: Client case repository
    """
    return SQLAlchemyClientCaseRepository(db)


def get_client_service(
    client_repo: SQLAlchemyClientRepository = Depends(get_client_repository),
    client_case_repo: SQLAlchemyClientCaseRepository = Depends(get_client_case_repository)
):
    """
    Get client service
    
    Args:
        client_repo: Client repository
        client_case_repo: Client case repository
        
    Returns:
        ClientService: Client service
    """
    return ClientService(client_repo, client_case_repo)