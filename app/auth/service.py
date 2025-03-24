# app/auth/service.py
"""
Authentication service for user authentication and authorization.
Handles user authentication, creation, and token management.
"""
from datetime import timedelta
from typing import Optional, Tuple, Dict, Any

from fastapi import HTTPException, status
from pydantic import BaseModel, Field, validator

from app.models import User, UserRole
from app.auth.security import PasswordService, TokenService
from app.auth.repository import UserRepositoryProtocol


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str
    role: UserRole

    @validator('role')
    def validate_role(cls, v):
        if v not in [UserRole.admin, UserRole.case_worker]:
            raise ValueError('Role must be either admin or case_worker')
        return v


class UserResponse(BaseModel):
    username: str
    email: str
    role: UserRole

    class Config:
        from_attributes = True


class AuthenticationService:
    """Service for user authentication and authorization"""
    
    def __init__(self, user_repository: UserRepositoryProtocol):
        self.user_repository = user_repository
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user with username and password
        
        Args:
            username: The username
            password: The plain text password
            
        Returns:
            Optional[User]: The authenticated user if successful, None otherwise
        """
        user = self.user_repository.get_by_username(username)
        if not user or not PasswordService.verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_user(self, user_data: UserCreate) -> User:
        """
        Create a new user
        
        Args:
            user_data: The user data
            
        Returns:
            User: The created user
            
        Raises:
            HTTPException: If username or email already exists
        """
        # Check if username exists
        if self.user_repository.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email exists
        if self.user_repository.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = PasswordService.get_password_hash(user_data.password)
        
        try:
            return self.user_repository.create(
                username=user_data.username,
                email=user_data.email,
                hashed_password=hashed_password,
                role=user_data.role
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e)
            )
    
    def create_access_token(self, username: str) -> Dict[str, Any]:
        """
        Create access token for a user
        
        Args:
            username: The username
            
        Returns:
            Dict[str, Any]: Access token response
        """
        access_token_expires = timedelta(minutes=30)  # Could be configurable
        access_token = TokenService.create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


class AuthorizationService:
    """Service for user authorization"""
    
    def __init__(self, user_repository: UserRepositoryProtocol):
        self.user_repository = user_repository
    
    def get_current_user(self, token_data: str) -> User:
        """
        Get the current user from a token
        
        Args:
            token_data: The token data with username
            
        Returns:
            User: The current user
            
        Raises:
            HTTPException: If user not found
        """
        user = self.user_repository.get_by_username(token_data.username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    
    def check_admin_role(self, user: User) -> None:
        """
        Check if user has admin role
        
        Args:
            user: The user to check
            
        Raises:
            HTTPException: If user is not an admin
        """
        if user.role != UserRole.admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admin users can perform this operation"
            )