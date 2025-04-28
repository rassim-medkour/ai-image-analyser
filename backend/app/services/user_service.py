"""
UserService: Contains business logic for user operations.
Orchestrates calls to UserRepository and handles validation, password hashing, etc.
"""
from app.repositories.user_repository import UserRepository
from app.models.user import User
from flask_jwt_extended import create_access_token

class UserService:
    @staticmethod
    def register_user(data):
        """
        Register a new user:
        - Expects a dict of validated data (username, email, password)
        - Check for existing username/email
        - Hash password
        - Save user to DB
        - Return a tuple: (user, access_token, error_message)
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
        access_token = create_access_token(identity=str(user.id))
        return user, access_token, None 

    @staticmethod
    def authenticate_user(data):
        """
        Authenticate user by username/email and password.
        - Expects a dict with 'username_or_email' and 'password'.
        - Determines if input is email or username.
        - Looks up user accordingly and checks password.
        - Returns (user, access_token, None) if successful, (None, None, error) otherwise.
        """
        username_or_email = data["username_or_email"]
        password = data["password"]

        if "@" in username_or_email:
            user = UserRepository.get_by_email(username_or_email)
        else:
            user = UserRepository.get_by_username(username_or_email)

        if not user or not user.check_password(password):
            return None, None, "Invalid credentials."
        access_token = create_access_token(identity=str(user.id))
        return user, access_token, None

    @staticmethod
    def get_user_profile(user_id):
        """Return user profile data."""
        return UserRepository.get_by_id(user_id)

    @staticmethod
    def list_users():
        """List all users."""
        return UserRepository.list_all()
