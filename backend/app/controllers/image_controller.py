from app.services.image_service import ImageService
from app.schemas.image_schema import ImageSchema

def upload_image(user_id, file_storage, metadata=None):
    """
    Controller logic for image upload:
    - Receives user_id (from JWT), file_storage (from request.files), and optional metadata (from request.form or JSON)
    - Validates file type/size if needed
    - Calls ImageService.upload_image
    - Returns serialized image or error message
    """
    if not file_storage:
        return {"errors": "No file provided."}, 400
    # Optionally: validate file type/size here (e.g., check allowed extensions, max size)
    original_filename = file_storage.filename
    content_type = file_storage.mimetype
    image, error = ImageService.upload_image(
        user_id=user_id,
        file_obj=file_storage,
        original_filename=original_filename,
        content_type=content_type,
        metadata=metadata
    )
    if error:
        return {"errors": error}, 400
    image_data = ImageSchema().dump(image)
    return image_data, 201
