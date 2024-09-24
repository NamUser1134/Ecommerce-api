# app/routes/category_routes.py
from flask import Blueprint, jsonify, request
from app.models.category import get_all_categories, get_category_by_id, add_category, delete_category
from app import categories_collection, products_collection
from bson import ObjectId

category_bp = Blueprint('category_bp', __name__)

def serialize_category(category):
    # Chuyển đổi ObjectId thành chuỗi
    if category and '_id' in category:
        category['_id'] = str(category['_id'])
    return category

def serialize_product(product):
    # Chuyển đổi ObjectId thành chuỗi
    if product and '_id' in product:
        product['_id'] = str(product['_id'])
    return product

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = get_all_categories()
    return jsonify([serialize_category(category) for category in categories])

@category_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    try:
        category = get_category_by_id(category_id)
        if category:
            return jsonify(serialize_category(category))
        else:
            return jsonify({"error": "Category not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@category_bp.route('/categories', methods=['POST'])
def create_category():
    try:
        data = request.json
        new_category = {
            "id": data['id'],
            "name": data['name'],
            "description": data['description']
        }
        add_category(new_category)
        return jsonify({"message": "Category created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@category_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category_route(category_id):
    try:
        delete_category(category_id)
        return jsonify({"message": "Category deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@category_bp.route('/categories/<int:category_id>/products', methods=['GET'])
def get_products_by_category(category_id):
    try:
        # Get page and per_page from query parameters with default values
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        # Calculate the number of products to skip
        skip = (page - 1) * per_page

        # Fetch products from MongoDB with pagination
        products_cursor = products_collection.find({"category_id": category_id}).skip(skip).limit(per_page)
        products = list(products_cursor)

        # Serialize and return the products
        return jsonify([serialize_product(product) for product in products])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
