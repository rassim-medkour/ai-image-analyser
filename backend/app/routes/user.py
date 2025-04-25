# Blueprint for user endpoints (profile, update, etc.)
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.schemas.user_schema import UserSchema
from flask import jsonify

user_bp = Blueprint("user", __name__)

@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_my_profile():
    user_id = get_jwt_identity()
    user = UserService.get_user_profile(user_id)
    if not user:
        return jsonify({"errors": "User not found."}), 404
    user_data = UserSchema().dump(user)
    return jsonify(user_data), 200

""" @user_bp.route('/', methods=['GET'])
@jwt_required()
def list_users():
    # Optionally restrict to admin users only
    users = UserService.list_users()
    user_data = UserSchema(many=True).dump(users)
    return jsonify(user_data), 200 """
