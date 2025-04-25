"""
UserService: Contains business logic for user operations.
Orchestrates calls to UserRepository and handles validation, password hashing, etc.
"""
from app.repositories.user_repository import UserRepository
from app.models.user import User

class UserService:
    @staticmethod
    def register_user(data):
        """
        Register a new user:
        - Expects a dict of validated data (username, email, password)
        - Check for existing username/email
        - Hash password
        - Save user to DB
        - Return user or error message
        """
        username = data["username"]
        email = data["email"]
        password = data["password"]

        if UserRepository.get_by_username(username):
            return None, "Username already exists."
        if UserRepository.get_by_email(email):
            return None, "Email already exists."

        user = User(username=username, email=email)
        user.set_password(password)
        UserRepository.create(user)
        return user, None

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
