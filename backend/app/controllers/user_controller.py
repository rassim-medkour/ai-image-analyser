from app.schemas.user_registration_schema import UserRegistrationSchema
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema
from marshmallow import ValidationError

def register_user(request_data):
    """
    Controller logic for user registration:
    - Validate input using UserRegistrationSchema
    - Call UserService.register_user
    - Return serialized user or error message
    """
    schema = UserRegistrationSchema()
    try:
        validated_data = schema.load(request_data)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    user, error = UserService.register_user(validated_data)
    if error:
        return {"errors": error}, 409

    user_data = UserSchema().dump(user)
    return user_data, 201
