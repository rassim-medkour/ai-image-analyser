"""
UserService: Contains business logic for user operations.
Orchestrates calls to UserRepository and handles validation, password hashing, etc.
"""
from app.repositories.user_repository import UserRepository
from app.models.user import User

class UserService:
    @staticmethod
    def register_user(username, email, password):
        """Register a new user, hash password, and save to DB."""
        # Business logic: check for existing user, hash password, etc.
        pass

    @staticmethod
    def authenticate_user(username_or_email, password):
        """Authenticate user by username/email and password."""
        # Business logic: fetch user, check password, return user or None
        pass

    @staticmethod
    def get_user_profile(user_id):
        """Return user profile data."""
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def list_users():
        """List all users."""
        return UserRepository.list_all()
