from app.schemas.user_login_schema import UserLoginSchema
from app.schemas.user_registration_schema import UserRegistrationSchema
from marshmallow import ValidationError
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema

def login_user(request_data):
    """
    Controller logic for user login:
    - Validate input using UserLoginSchema
    - Pass validated data dict to UserService.authenticate_user
    - Return user data and JWT or error message
    """
    schema = UserLoginSchema()
    try:
        validated_data = schema.load(request_data)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    user, access_token, error = UserService.authenticate_user(validated_data)
    if error:
        return {"errors": error}, 401

    user_data = UserSchema().dump(user)
    return {"user": user_data, "access_token": access_token}, 200


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

    user, access_token, error = UserService.register_user(validated_data)
    if error:
        return {"errors": error}, 409

    user_data = UserSchema().dump(user)
    return {"user": user_data, "access_token": access_token}, 201
