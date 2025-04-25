"""
ImageService: Contains business logic for image operations.
Orchestrates calls to ImageRepository and handles S3/R2 integration, validation, etc.
"""
from app.utils.s3_helper import S3Helper
from flask import current_app
from app.repositories.image_repository import ImageRepository
from app.models.image import Image
from app.repositories.image_repository import ImageRepository

class ImageService:
    @staticmethod
    def upload_image(user_id, file_obj, original_filename, content_type, metadata=None):
        """
        Upload an image to S3/R2 and create a DB record.
        - user_id: ID of the uploading user
        - file_obj: file-like object (from Flask request.files)
        - original_filename: original file name
        - content_type: MIME type
        - metadata: optional dict for extra info
        Returns: (Image instance, error message or None)
        """
        # Generate a unique S3 key (e.g., user_id/timestamp/filename)
        import uuid, time
        s3_key = f"{user_id}/{int(time.time())}_{uuid.uuid4().hex}_{original_filename}"
        s3_helper = S3Helper()
        try:
            s3_url = s3_helper.upload_file(file_obj, s3_key, content_type)
        except Exception as e:
            return None, f"Image upload failed: {str(e)}"

        file_obj.seek(0, 2)  # Move to end to get size
        file_size = file_obj.tell()
        file_obj.seek(0)
        image = Image(
            filename=s3_key,
            original_filename=original_filename,
            s3_url=s3_url,
            s3_key=s3_key,
            upload_date=None,  # Let DB default handle
            file_size=file_size,
            file_type=content_type,
            ai_description=metadata.get('ai_description') if metadata else None,
            user_id=user_id
        )
        ImageRepository.create(image)
        return image, None

    @staticmethod
    def delete_image(user_id, image_id):
        """
        Delete an image from S3/R2 and remove the DB record.
        - Checks ownership before deletion.
        Returns: (True, None) on success, (False, error message) on failure
        """
        image = ImageRepository.get_by_id(image_id)
        if not image:
            return False, "Image not found."
        if image.user_id != user_id:
            return False, "Unauthorized to delete this image."
        s3_helper = S3Helper()
        try:
            s3_helper.delete_file(image.s3_key)
        except Exception as e:
            return False, f"S3 delete failed: {str(e)}"
        ImageRepository.delete(image)
        return True, None

    @staticmethod
    def list_user_images(user_id):
        """List all images for a user."""
        return ImageRepository.list_by_user(user_id)

    @staticmethod
    def get_image(user_id, image_id):
        """Get image metadata by ID and User ID."""
        return ImageRepository.get_by_id_and_user(image_id, user_id)
