"""
ImageRepository: Implements the Repository pattern for image data persistence operations.
The Repository pattern abstracts database operations and provides a collection-like
interface for accessing domain objects (Images). This decouples the application logic 
from specific database implementation details, facilitating:

1. Centralized data access logic
2. Easier unit testing through potential mocking
3. Simplified switching of data sources if needed
"""
from app.models.image import Image
from app import db

class ImageRepository:
    """
    Repository class for encapsulating storage, retrieval, and search operations
    related to Image entities. All database operations for Image models should 
    flow through this class to maintain consistent data access patterns.
    """

    @staticmethod
    def get_by_id(image_id):
        """
        Fetch an image by its primary key.
        
        Args:
            image_id: Primary key of the image to retrieve
            
        Returns:
            Image: Image instance if found, None otherwise
        """
        return Image.query.get(image_id)
    
    @staticmethod
    def get_by_id_and_user(image_id, user_id):
        """
        Fetch an image by ID only if it belongs to the specified user.
        Enforces object-level authorization within the data access layer.
        
        Args:
            image_id: Primary key of the image
            user_id: User ID to verify ownership
            
        Returns:
            Image: Image instance if found and owned by user, None otherwise
        """
        return Image.query.filter_by(id=image_id, user_id=user_id).first()

    @staticmethod
    def list_by_user(user_id):
        """
        List all images belonging to a specific user.
        Provides data filtering at the repository level for security.
        
        Args:
            user_id: ID of the user whose images to retrieve
            
        Returns:
            list: Collection of Image instances for the user
        """
        return Image.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create(image):
        """
        Add a new image to the database and persist changes.
        
        Args:
            image: Image model instance to persist
            
        Returns:
            Image: The persisted Image instance with populated ID
        """
        db.session.add(image)
        db.session.commit()
        return image

    @staticmethod
    def delete(image):
        """
        Delete an image from the database and persist changes.
        
        Args:
            image: Image model instance to delete
        """
        db.session.delete(image)
        db.session.commit()

    @staticmethod
    def list_all():
        """
        List all images regardless of ownership.
        Typically used for administrative functions.
        
        Returns:
            list: Collection of all Image instances in the database
        """
        return Image.query.all()
