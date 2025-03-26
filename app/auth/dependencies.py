# app/auth/dependencies.py
"""
Authentication dependencies for FastAPI dependency injection.
Provides injectable dependencies for current user, admin user, etc.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.auth.repository import SQLAlchemyUserRepository
from app.auth.service import AuthorizationService
from app.auth.security import TokenService

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_user_repository(db: Session = Depends(get_db)):
    """
    Get the user repository
    
    Args:
        db: The database session
        
    Returns:
        SQLAlchemyUserRepository: The user repository
    """
    return SQLAlchemyUserRepository(db)


def get_authorization_service(repository = Depends(get_user_repository)):
    """
    Get the authorization service
    
    Args:
        repository: The user repository
        
    Returns:
        AuthorizationService: The authorization service
    """
    return AuthorizationService(repository)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthorizationService = Depends(get_authorization_service)
) -> User:
    """
    Get the current user from the token
    
    Args:
        token: The JWT token
        auth_service: The authorization service
        
    Returns:
        User: The current user
        
    Raises:
        HTTPException: If token validation fails
    """
    token_data = TokenService.decode_token(token)
    return auth_service.get_current_user(token_data)


async def get_admin_user(
    current_user: User = Depends(get_current_user),
    auth_service: AuthorizationService = Depends(get_authorization_service)
) -> User:
    """
    Ensure the current user is an admin
    
    Args:
        current_user: The current user
        auth_service: The authorization service
        
    Returns:
        User: The current admin user
        
    Raises:
        HTTPException: If user is not an admin
    """
    auth_service.check_admin_role(current_user)
    return current_user