# app/auth/router.py
"""
Router for authentication endpoints.
Handles login, user creation, and other auth-related routes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.service import AuthenticationService, UserCreate, UserResponse
from app.auth.dependencies import get_user_repository, get_admin_user
from app.models import User

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthenticationService = Depends(
        lambda repo=Depends(get_user_repository): AuthenticationService(repo)
    )
):
    """
    Login endpoint to get access token
    
    Args:
        form_data: The login form data
        auth_service: The authentication service
        
    Returns:
        dict: Access token response
        
    Raises:
        HTTPException: If authentication fails
    """
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_service.create_access_token(user.username)


@router.post("/users", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    current_user: User = Depends(get_admin_user),
    auth_service: AuthenticationService = Depends(
        lambda repo=Depends(get_user_repository): AuthenticationService(repo)
    )
):
    """
    Create a new user (admin only)
    
    Args:
        user_data: The user data
        current_user: The current admin user
        auth_service: The authentication service
        
    Returns:
        UserResponse: The created user
        
    Raises:
        HTTPException: If user creation fails
    """
    return auth_service.create_user(user_data)