from flask import request, jsonify
from app import app, products_collection
from bson import json_util, ObjectId
import json
from datetime import datetime, timezone

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the E-commerce API"}), 200

@app.route('/product', methods=['POST'])
def create_product():
    try:
        # Lấy dữ liệu từ request
        product_data = request.json

        # Kiểm tra dữ liệu đầu vào
        if not product_data or not isinstance(product_data, dict):
            return jsonify({"error": "Invalid input data"}), 400

        required_fields = ['name', 'price', 'description']
        for field in required_fields:
            if field not in product_data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
            
            
        # Tự động tạo created_at và release_date nếu không có trong request
        current_time = datetime.now(timezone.utc)  # Get current time in UTC
        product_data['created_at'] = product_data.get('created_at', current_time.isoformat())
        product_data['release_date'] = product_data.get('release_date', current_time.isoformat())

        # Thêm sản phẩm vào database
        result = products_collection.insert_one(product_data)

        # Trả về kết quả
        return jsonify({
            "message": "Product created successfully",
            "id": str(result.inserted_id)
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/products', methods=['GET'])
def get_products():
    try:
        products = list(products_collection.find())
        return json.loads(json_util.dumps(products)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/product/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        if product:
            return json.loads(json_util.dumps(product)), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/product/<product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        product_data = request.json

        # Tự động tạo created_at và release_date nếu không có trong request
        current_time = datetime.now(timezone.utc)  # Get current time in UTC
        if 'created_at' not in product_data:
            product_data['created_at'] = current_time.isoformat()
        if 'release_date' not in product_data:
            product_data['release_date'] = current_time.isoformat()

        result = products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": product_data}
        )
        if result.modified_count:
            return jsonify({"message": "Product updated successfully"}), 200
        else:
            return jsonify({"error": "Product not found or no changes made"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        result = products_collection.delete_one({"_id": ObjectId(product_id)})
        if result.deleted_count:
            return jsonify({"message": "Product deleted successfully"}), 200
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route to get all "coming soon" products
@app.route('/products/coming-soon', methods=['GET'])
def get_coming_soon_products():
    try:
        coming_soon_products = list(products_collection.find({"is_coming_soon": True}))
        return json.loads(json_util.dumps(coming_soon_products)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Route to get all "latest product" products
@app.route('/products/latest', methods=['GET'])
def get_latest_products():
    try:
        latest_products = list(products_collection.find({"is_coming_soon": False}))
        return json.loads(json_util.dumps(latest_products)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500