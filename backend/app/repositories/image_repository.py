"""
ImageRepository: Handles all database operations for the Image model.
"""
from app.models.image import Image
from app import db

class ImageRepository:
    @staticmethod
    def get_by_id(image_id):
        """Fetch an image by primary key."""
        return Image.query.get(image_id)
    
    @staticmethod
    def get_by_id_and_user(image_id, user_id):
        return Image.query.filter_by(id=image_id, user_id=user_id).first()

    @staticmethod
    def list_by_user(user_id):
        """List all images belonging to a user."""
        return Image.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create(image):
        """Add a new image to the database."""
        db.session.add(image)
        db.session.commit()
        return image

    @staticmethod
    def delete(image):
        """Delete an image from the database."""
        db.session.delete(image)
        db.session.commit()

    @staticmethod
    def list_all():
        """List all images."""
        return Image.query.all()
