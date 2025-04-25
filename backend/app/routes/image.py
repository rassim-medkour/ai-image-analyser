# Blueprint for image endpoints (upload, list, etc.)
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.image_controller import upload_image, get_image, get_all_images, delete_image

image_bp = Blueprint("image", __name__)

@image_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    user_id = get_jwt_identity()
    file_storage = request.files.get('file')
    # Optionally, parse metadata from form or JSON
    metadata = request.form.to_dict() if request.form else None
    response, status = upload_image(user_id, file_storage, metadata)
    return jsonify(response), status

@image_bp.route('/<int:image_id>', methods=['GET'])
@jwt_required()
def get_single_image(image_id):
    user_id = get_jwt_identity()
    response, status = get_image(user_id, image_id)
    return jsonify(response), status

@image_bp.route('/', methods=['GET'])
@jwt_required()
def list_images():
    user_id = get_jwt_identity()
    response, status = get_all_images(user_id)
    return jsonify(response), status

@image_bp.route('/<int:image_id>', methods=['DELETE'])
@jwt_required()
def delete(image_id):
    user_id = get_jwt_identity()
    response, status = delete_image(user_id, image_id)
    return jsonify(response), status
