from app.schemas.user_registration_schema import UserRegistrationSchema
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema
from marshmallow import ValidationError


def get_user_profile(user_id):
    """
    Controller logic to get a user profile by user_id.
    - Calls UserService.get_user_profile
    - Returns serialized user or error message
    """
    user = UserService.get_user_profile(user_id)
    if not user:
        return {"errors": "User not found."}, 404
    user_data = UserSchema().dump(user)
    return user_data, 200


""" def list_users():
 """    """
    #Controller logic to list all users.
    #- Calls UserService.list_users
    #- Returns a list of serialized users
    """
"""     users = UserService.list_users()
    user_data = UserSchema(many=True).dump(users)
    return user_data, 200 """

