from app.schemas.user_login_schema import UserLoginSchema
from app.services.user_service import UserService
from marshmallow import ValidationError

def login_user(request_data):
    """
    Controller logic for user login:
    - Validate input using UserLoginSchema
    - Check user existence and password correctness via UserService
    - Return user data or error message
    """
    schema = UserLoginSchema()
    try:
        validated_data = schema.load(request_data)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    user, error = UserService.authenticate_user(
        validated_data["username_or_email"],
        validated_data["password"]
    )
    if error:
        return {"errors": error}, 401

    # For now, just return user data (no JWT yet)
    from app.schemas.user_schema import UserSchema
    user_data = UserSchema().dump(user)
    return user_data, 200
