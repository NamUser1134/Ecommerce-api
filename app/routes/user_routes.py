# app/routes/user_routes.py
from flask import Blueprint, jsonify, request
from app.models.user import User
from app.models.image import Image
from app import users_collection, images_collection
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bson import ObjectId, json_util
import os
import base64
import json

user_bp = Blueprint('user_bp', __name__)

# Register a new user with an image and role
@user_bp.route('/register', methods=['POST'])
def register():
    try:
        user_data = request.form.to_dict()
        required_fields = ['email', 'password', 'name']

        # Validate required fields
        for field in required_fields:
            if field not in user_data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Check if email already exists
        if User.find_by_email(users_collection, user_data['email']):
            return jsonify({"error": "Email already exists"}), 400

        # Handle the image file if provided
        if 'image' in request.files:
            image_file = request.files['image']
            image_id = Image.create(images_collection, {}, image_file)
            user_data['image_id'] = image_id  # Link user to image
        
        # Create the user
        user_id = User.create(users_collection, user_data)
        return jsonify({"message": "User registered successfully", "id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# User login route
@user_bp.route('/login', methods=['POST'])
def login():
    try:
        login_data = request.json
        email = login_data.get('email')
        password = login_data.get('password')

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        user = User.find_by_email(users_collection, email)
        if not user or not User.check_password(user, password):
            return jsonify({"error": "Invalid email or password"}), 401

        # Customize fields in the token
        custom_claims = {
            "user_id": str(user['_id']), 
            "name": user['name'],
            "role": user['role'],
            "image_id": user['image_id']
        }
        access_token = create_access_token(identity=custom_claims)
        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get user details (JWT required)
@user_bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    try:
        claims = get_jwt_identity()
        user_id = claims['user_id']
        user = User.find_by_id(users_collection, user_id)

        if user:
            return json.loads(json_util.dumps(user)), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update an existing user with an image and role
@user_bp.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user_data = request.form.to_dict()

        # Update the user's image if provided
        if 'image' in request.files:
            image_file = request.files['image']
            
            # If the user already has an image, update the existing one
            user = User.find_by_id(users_collection, user_id)
            if user and 'image_id' in user:
                Image.update(images_collection, user['image_id'], image_file)
            else:
                # If no image exists, create a new image entry
                image_id = Image.create(images_collection, {}, image_file)
                user_data['image_id'] = image_id
        
        # Update user details
        User.update(users_collection, user_id, user_data)
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Delete user by ID (No JWT required)
@user_bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # Delete user by ID
        User.delete(users_collection, user_id)
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

