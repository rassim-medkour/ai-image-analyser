"""
ImageService: Contains business logic for image operations.
Orchestrates calls to ImageRepository and handles S3/R2 integration, validation, etc.
"""
from app.repositories.image_repository import ImageRepository
from app.models.image import Image

class ImageService:
    @staticmethod
    def upload_image(user_id, file_data, metadata):
        """Handle image upload, S3/R2 storage, and DB record creation."""
        # Business logic: upload to S3, create Image record, etc.
        pass

    @staticmethod
    def list_user_images(user_id):
        """List all images for a user."""
        return ImageRepository.list_by_user(user_id)

    @staticmethod
    def delete_image(image_id):
        """Delete image from S3/R2 and remove DB record."""
        # Business logic: delete from S3, remove Image record, etc.
        pass

    @staticmethod
    def get_image(image_id):
        """Get image metadata by ID."""
        return ImageRepository.get_by_id(image_id)
