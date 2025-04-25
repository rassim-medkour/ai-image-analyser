"""
UserRepository: Handles all database operations for the User model.
"""
from app.models.user import User
from app import db

class UserRepository:
    @staticmethod
    def get_by_id(user_id):
        """Fetch a user by primary key."""
        return User.query.get(user_id)

    @staticmethod
    def get_by_username(username):
        """Fetch a user by username."""
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_email(email):
        """Fetch a user by email."""
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create(user):
        """Add a new user to the database."""
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def delete(user):
        """Delete a user from the database."""
        db.session.delete(user)
        db.session.commit()

    @staticmethod
    def list_all():
        """List all users."""
        return User.query.all()
