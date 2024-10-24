from flask import Blueprint, jsonify, request
from app.models.image import Image
from app import images_collection
from bson import ObjectId

image_bp = Blueprint('image_bp', __name__)

# Add a new image (No JWT, no ID required)
@image_bp.route('/images', methods=['POST'])
def add_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "Image file is required"}), 400

        image_file = request.files['image']
        image_data = {}

        # Save the image to database as base64
        image_id = Image.create(images_collection, image_data, image_file)
        return jsonify({"message": "Image uploaded", "image_id": image_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update an image by ID (No JWT required)
@image_bp.route('/images/<image_id>', methods=['PUT'])
def update_image(image_id):
    try:
        if 'image' not in request.files:
            return jsonify({"error": "Image file is required"}), 400

        image_file = request.files['image']
        Image.update(images_collection, image_id, image_file)
        return jsonify({"message": "Image updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete an image by ID (No JWT required)
@image_bp.route('/images/<image_id>', methods=['DELETE'])
def delete_image(image_id):
    try:
        Image.delete(images_collection, image_id)
        return jsonify({"message": "Image deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
