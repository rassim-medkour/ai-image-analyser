"""
ImageService: Central service for image operations in the application.
Implements a facade pattern that orchestrates interactions between:
- S3/R2 cloud storage (via S3Helper)
- Image analysis (via ImageAnalysisService and Strategy pattern)
- Database operations (via ImageRepository)

This service separates business logic from controllers and repositories,
enforcing proper separation of concerns in the application architecture.
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
        Initialize the ImageService with optional dependency injection.
        Follows dependency injection pattern to facilitate unit testing
        and improve module decoupling.
        
        Args:
            analysis_service: Optional ImageAnalysisService instance for AI analysis
            analysis_strategy: Optional AnalysisStrategy instance for analysis method selection
        """
        # Dependency injection for the analysis service
        if analysis_service is None:
            # Only create a default if none was provided
            analysis_provider = current_app.config.get('IMAGE_ANALYSIS_PROVIDER', 'clarifai')
            self.analysis_service = ImageAnalysisService(provider=analysis_provider)
        else:
            self.analysis_service = analysis_service
            
        # Dependency injection for the analysis strategy
        # Default to FallbackAnalysisStrategy for maximum reliability
        self.analysis_strategy = analysis_strategy or FallbackAnalysisStrategy()

    def upload_image(self, user_id, file_obj, original_filename, content_type, metadata=None):
        """
        Complete image upload workflow:
        1. Generate unique storage key
        2. Upload file to cloud storage (S3/R2)
        3. Perform AI analysis of content using selected strategy
        4. Store metadata and analysis results in database
        
        Args:
            user_id: ID of the uploading user (for permission and organization)
            file_obj: File-like object from request (implements read() method)
            original_filename: Original uploaded filename (for display)
            content_type: MIME type of the file
            metadata: Optional dictionary of additional metadata
            
        Returns:
            tuple: (Image model instance, error message or None)
        """
        # Generate a unique S3 key with user scoping and timestamp
        # Format: {user_id}/{timestamp}_{uuid}_{filename}
        s3_key = f"{user_id}/{int(time.time())}_{uuid.uuid4().hex}_{original_filename}"
        
        # Get file size for database storage before reading content
        file_obj.seek(0, 2)  # Move to end to get size
        file_size = file_obj.tell()
        file_obj.seek(0)  # Reset to beginning of file
        
        # Read file content for analysis while preserving file pointer
        file_content = file_obj.read()
        file_obj.seek(0)  # Reset pointer for S3 upload
        
        # Upload to S3/R2 storage
        s3_helper = S3Helper()
        try:
            s3_url = s3_helper.upload_file(file_obj, s3_key, content_type)
        except Exception as e:
            # Early return if storage upload fails
            return None, f"Image upload failed: {str(e)}"
        
        # Initialize AI description field
        ai_description = None
        
        # Analyze the image with AI service using the strategy pattern
        try:
            # Create a pre-signed URL with 1-hour expiration for external services
            analysis_url = s3_helper.get_presigned_url(s3_key, expires=3600)
            
            # Use the analysis strategy to handle the analysis workflow
            # Strategy pattern delegates decision making about using URL vs bytes
            analysis_result = self.analysis_strategy.analyze(
                analysis_service=self.analysis_service,
                image_bytes=file_content,
                image_url=analysis_url
            )
                
            # Extract the AI-generated description with error handling
            if analysis_result.get('description') and not analysis_result.get('using_fallback', False):
                ai_description = analysis_result['description']
                current_app.logger.info(f"Generated AI description: {ai_description}")
            elif analysis_result.get('using_fallback'):
                current_app.logger.warning(f"Using fallback response: {analysis_result.get('error')}")
            else:
                current_app.logger.warning("Failed to generate AI description")
        except Exception as e:
            # Log the error but continue with upload process
            # This ensures upload succeeds even if AI analysis fails
            current_app.logger.error(f"AI analysis error: {str(e)}")

        # Create image record in database with all collected metadata
        image = Image(
            filename=s3_key,
            original_filename=original_filename,
            s3_key=s3_key,
            upload_date=None,  # Let DB default handle with current timestamp
            file_size=file_size,
            file_type=content_type,
            ai_description=ai_description,  # May be None if analysis failed
            user_id=user_id
        )
        
        # Persist to database
        ImageRepository.create(image)
        return image, None

    def delete_image(self, user_id, image_id):
        """
        Delete an image completely from both storage and database.
        Includes ownership verification for security.
        
        Args:
            user_id: ID of the requesting user (for permission check)
            image_id: Database ID of the image to delete
            
        Returns:
            tuple: (success boolean, error message or None)
        """
        # Get image record from database
        image = ImageRepository.get_by_id(image_id)
        
        # Handle non-existent image
        if not image:
            return False, "Image not found."
            
        # Security check: verify ownership before deletion
        if image.user_id != user_id:
            return False, "Unauthorized to delete this image."
            
        # Delete from S3/R2 storage first
        s3_helper = S3Helper()
        try:
            s3_helper.delete_file(image.s3_key)
        except Exception as e:
            return False, f"S3 delete failed: {str(e)}"
            
        # If storage deletion successful, remove database record
        ImageRepository.delete(image)
        return True, None

    def list_user_images(self, user_id):
        """
        Retrieve all images belonging to a specific user.
        
        Args:
            user_id: ID of the user whose images to retrieve
            
        Returns:
            list: Collection of Image model instances
        """
        return ImageRepository.list_by_user(user_id)

    def get_image(self, user_id, image_id):
        """
        Get a specific image with ownership verification.
        
        Args:
            user_id: ID of the requesting user (for permission check)
            image_id: Database ID of the requested image
            
        Returns:
            Image: The requested image if found and owned by user, None otherwise
        """
        return ImageRepository.get_by_id_and_user(image_id, user_id)
