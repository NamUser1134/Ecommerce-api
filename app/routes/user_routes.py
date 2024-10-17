from flask import Blueprint, jsonify, request
from app.models.user import User
from app import users_collection
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bson import json_util, ObjectId
import json

user_bp = Blueprint('user_bp', __name__)

# Register a new user
@user_bp.route('/register', methods=['POST'])
def register():
    try:
        user_data = request.json
        required_fields = ['email', 'password', 'name']

        for field in required_fields:
            if field not in user_data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        if User.find_by_email(users_collection, user_data['email']):
            return jsonify({"error": "Email already exists"}), 400

        user_id = User.create(users_collection, user_data)
        return jsonify({"message": "User registered successfully", "id": user_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Login user
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

        # Tùy chỉnh các trường trong access_token
        custom_claims = {
            "user_id": str(user['_id']),
            "name": user['name'],
            # Thêm các trường khác mà bạn muốn đưa vào token
        }
        access_token = create_access_token(identity=custom_claims)
        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500# Get user details (protected route)
    
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

# Update user (protected route)
@user_bp.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user_data = request.json

        # Update user information
        User.update(users_collection, user_id, user_data)
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
# Delete user (protected route)
@user_bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # Xóa người dùng theo ID
        User.delete(users_collection, user_id)
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
