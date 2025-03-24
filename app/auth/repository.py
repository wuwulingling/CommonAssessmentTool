"""
Repository for user data access operations.
Implements the repository pattern for user-related database operations.
"""
from typing import Optional, Protocol, List
from sqlalchemy.orm import Session
from app.models import User, UserRole


class UserRepositoryProtocol(Protocol):
    """Protocol defining the interface for user repositories"""
    
    def get_by_username(self, username: str) -> Optional[User]: ...
    def get_by_email(self, email: str) -> Optional[User]: ...
    def create(self, username: str, email: str, hashed_password: str, role: UserRole) -> User: ...
    def get_all(self) -> List[User]: ...


class SQLAlchemyUserRepository:
    """SQLAlchemy implementation of the user repository"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_username(self, username: str) -> Optional[User]:
        """
        Get a user by username
        
        Args:
            username: The username to search for
            
        Returns:
            Optional[User]: The user if found, None otherwise
        """
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email
        
        Args:
            email: The email to search for
            
        Returns:
            Optional[User]: The user if found, None otherwise
        """
        return self.db.query(User).filter(User.email == email).first()
    
    def create(self, username: str, email: str, hashed_password: str, role: UserRole) -> User:
        """
        Create a new user
        
        Args:
            username: The username
            email: The email
            hashed_password: The hashed password
            role: The user role
            
        Returns:
            User: The created user
            
        Raises:
            Exception: If user creation fails
        """

        # Check if username exists
        if self.get_by_username(username):
            raise ValueError("Username already exists")

        # Check if email exists
        if self.get_by_email(email):
            raise ValueError("Email already exists")
    
        db_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role=role
        )
        
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except Exception as e:
            self.db.rollback()
            # Convert database errors to domain-specific errors
            if "UNIQUE constraint failed: users.username" in str(e):
                raise ValueError("Username already exists")
            if "UNIQUE constraint failed: users.email" in str(e):
                raise ValueError("Email already exists")
            raise e
    
    def get_all(self) -> List[User]:
        """
        Get all users
        
        Returns:
            List[User]: All users in the database
        """
        return self.db.query(User).all()