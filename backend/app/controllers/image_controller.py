from app.services.image_service import ImageService
from app.schemas.image_schema import ImageSchema

def upload_image(user_id, file_storage, metadata=None):
    """
    Controller function that handles image upload requests.
    Acts as a thin layer between HTTP requests and service logic, responsible for:
    - Input validation and sanitization
    - Invoking the appropriate service operations
    - Formatting the response data
    
    Args:
        user_id (int): User ID from JWT authentication
        file_storage: File object from Flask's request.files
        metadata (dict, optional): Additional metadata from request
        
    Returns:
        tuple: (response_data, http_status_code)
            - On success: (serialized_image, 201)
            - On failure: (error_dict, 400)
    """
    # Basic input validation
    if not file_storage:
        return {"errors": "No file provided."}, 400
        
    # Extract file metadata from the request
    original_filename = file_storage.filename
    content_type = file_storage.mimetype
    
    # Create an instance of ImageService to handle business logic
    image_service = ImageService()
    
    # Delegate to service layer for processing
    image, error = image_service.upload_image(
        user_id=user_id,
        file_obj=file_storage,
        original_filename=original_filename,
        content_type=content_type,
        metadata=metadata
    )
    
    # Handle errors from service layer
    if error:
        return {"errors": error}, 400
    
    # Serialize the model for API response using schema
    image_data = ImageSchema().dump(image)
    return image_data, 201


def get_image(user_id, image_id):
    """
    Controller function that retrieves a single image by ID.
    Enforces user authorization by checking ownership.
    
    Args:
        user_id (int): User ID from JWT authentication
        image_id (int): ID of the image to retrieve
        
    Returns:
        tuple: (response_data, http_status_code)
            - On success: (serialized_image, 200)
            - On failure: (error_dict, 404)
    """
    image_service = ImageService()
    
    # Request image with automatic ownership verification
    image = image_service.get_image(user_id, image_id)
    
    # Handle case when image doesn't exist or user doesn't have access
    if not image:
        return {"errors": "Image not found."}, 404
        
    # Serialize the model for API response
    image_data = ImageSchema().dump(image)
    return image_data, 200


def get_all_images(user_id):
    """
    Controller function that retrieves all images belonging to a user.
    Provides collection pagination capabilities.
    
    Args:
        user_id (int): User ID from JWT authentication
        
    Returns:
        tuple: (response_data, http_status_code)
            - Always returns: (serialized_images, 200)
            - Empty list if user has no images
    """
    image_service = ImageService()
    
    # Get all images for the user
    images = image_service.list_user_images(user_id)
    
    # Serialize collection of models (many=True)
    image_data = ImageSchema(many=True).dump(images)
    return image_data, 200


def delete_image(user_id, image_id):
    """
    Controller function that handles image deletion requests.
    Coordinates both database record removal and storage cleanup.
    
    Args:
        user_id (int): User ID from JWT authentication
        image_id (int): ID of the image to delete
        
    Returns:
        tuple: (response_data, http_status_code)
            - On success: (success_message, 200)
            - On failure: (error_dict, 400)
    """
    image_service = ImageService()
    
    # Attempt to delete image with all ownership checks
    success, error = image_service.delete_image(user_id, image_id)
    
    # Handle any errors from service layer
    if not success:
        return {"errors": error}, 400
        
    # Return success confirmation
    return {"message": "Image deleted successfully."}, 200
