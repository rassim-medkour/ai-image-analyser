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


def get_image(user_id, image_id):
    """
    Controller logic to get a single image by ID for a user.
    - Checks ownership.
    - Returns serialized image or error message.
    """
    from app.services.image_service import ImageService
    from app.schemas.image_schema import ImageSchema
    image = ImageService.get_image(user_id, image_id)
    if not image:
        return {"errors": "Image not found."}, 404
    image_data = ImageSchema().dump(image)
    return image_data, 200


def get_all_images(user_id):
    """
    Controller logic to get all images belonging to a user.
    - Returns a list of serialized images.
    """
    from app.services.image_service import ImageService
    from app.schemas.image_schema import ImageSchema
    images = ImageService.list_user_images(user_id)
    image_data = ImageSchema(many=True).dump(images)
    return image_data, 200
