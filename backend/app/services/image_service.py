"""
ImageService: Contains business logic for image operations.
Orchestrates calls to ImageRepository and handles S3/R2 integration, validation, etc.
"""
import uuid
import time
from flask import current_app
from app.utils.s3_helper import S3Helper
from app.repositories.image_repository import ImageRepository
from app.services.image_analysis_service import ImageAnalysisService
from app.services.analysis_strategies import FallbackAnalysisStrategy
from app.models.image import Image


class ImageService:
    def __init__(self, analysis_service=None, analysis_strategy=None):
        """
        Initialize the ImageService with optional dependencies.
        Args:
            analysis_service: An optional ImageAnalysisService instance
            analysis_strategy: An optional AnalysisStrategy instance
        """
        # Use dependency injection for the analysis service
        if analysis_service is None:
            # Only create a default if none was provided
            analysis_provider = current_app.config.get('IMAGE_ANALYSIS_PROVIDER', 'clarifai')
            self.analysis_service = ImageAnalysisService(provider=analysis_provider)
        else:
            self.analysis_service = analysis_service
            
        # Use dependency injection for the analysis strategy
        self.analysis_strategy = analysis_strategy or FallbackAnalysisStrategy()

    def upload_image(self, user_id, file_obj, original_filename, content_type, metadata=None):
        """
        Upload an image to S3/R2, analyze with AI service, and create a DB record.
        - user_id: ID of the uploading user
        - file_obj: file-like object (from Flask request.files)
        - original_filename: original file name
        - content_type: MIME type
        - metadata: optional dict for extra info
        Returns: (Image instance, error message or None)
        """
        # Generate a unique S3 key (e.g., user_id/timestamp/filename)
        s3_key = f"{user_id}/{int(time.time())}_{uuid.uuid4().hex}_{original_filename}"
        # Get file size first
        file_obj.seek(0, 2)  # Move to end to get size
        file_size = file_obj.tell()
        file_obj.seek(0)  # Reset to beginning of file
        # Read file content for analysis
        file_content = file_obj.read()
        file_obj.seek(0)  # Reset pointer for S3 upload
        # Upload to S3
        s3_helper = S3Helper()
        try:
            s3_url = s3_helper.upload_file(file_obj, s3_key, content_type)
        except Exception as e:
            return None, f"Image upload failed: {str(e)}"
        
        # Initialize ai_description to None
        ai_description = None
        
        # Analyze the image with AI service using the strategy pattern
        try:
            # Create a pre-signed URL with 1-hour expiration for Clarifai to access
            analysis_url = s3_helper.get_presigned_url(s3_key, expires=3600)
            
            # Use the analysis strategy to handle the analysis flow
            analysis_result = self.analysis_strategy.analyze(
                analysis_service=self.analysis_service,
                image_bytes=file_content,
                image_url=analysis_url
            )
                
            # Extract the generated description, handle fallbacks gracefully
            if analysis_result.get('description') and not analysis_result.get('using_fallback', False):
                ai_description = analysis_result['description']
                current_app.logger.info(f"Generated AI description: {ai_description}")
            elif analysis_result.get('using_fallback'):
                current_app.logger.warning(f"Using fallback response: {analysis_result.get('error')}")
            else:
                current_app.logger.warning("Failed to generate AI description")
        except Exception as e:
            # Log the error but continue with the upload process
            # This way, upload won't fail if AI analysis fails
            current_app.logger.error(f"AI analysis error: {str(e)}")

        # Create image record in database
        image = Image(
            filename=s3_key,
            original_filename=original_filename,
            s3_key=s3_key,
            upload_date=None,  # Let DB default handle
            file_size=file_size,
            file_type=content_type,
            ai_description=ai_description,  # Use AI-generated description if available
            user_id=user_id
        )
        ImageRepository.create(image)
        return image, None

    def delete_image(self, user_id, image_id):
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

    def list_user_images(self, user_id):
        """List all images for a user."""
        return ImageRepository.list_by_user(user_id)

    def get_image(self, user_id, image_id):
        """Get image metadata by ID and User ID."""
        return ImageRepository.get_by_id_and_user(image_id, user_id)
