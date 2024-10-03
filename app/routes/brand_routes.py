# app/routes/brand_routes.py
from flask import Blueprint, jsonify, request
from app.models.brand import get_all_brands, get_brand_by_id, add_brand, update_brand, delete_brand
from app import brands_collection, products_collection
from bson import ObjectId

brand_bp = Blueprint('brand_bp', __name__)

def serialize_brand(brand):
    if brand and '_id' in brand:
        brand['_id'] = str(brand['_id'])
    return brand

def serialize_product(product):
    if product and '_id' in product:
        product['_id'] = str(product['_id'])
    return product

# 1. Get All Brands
@brand_bp.route('/brands', methods=['GET'])
def get_brands():
    brands = get_all_brands()
    return jsonify([serialize_brand(brand) for brand in brands])

# 2. Get Brand by ID
@brand_bp.route('/brands/<int:brand_id>', methods=['GET'])
def get_brand(brand_id):
    try:
        brand = get_brand_by_id(brand_id)
        if brand:
            return jsonify(serialize_brand(brand))
        else:
            return jsonify({"error": "Brand not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. Create a Brand
@brand_bp.route('/brands', methods=['POST'])
def create_brand():
    try:
        data = request.json
        new_brand = {
            "id": data['id'],
            "name": data['name'],
            "description": data['description']
        }
        add_brand(new_brand)
        return jsonify({"message": "Brand created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 4. Update a Brand (New)
@brand_bp.route('/brands/<int:brand_id>', methods=['PUT'])
def update_brand_route(brand_id):
    try:
        data = request.json
        update_data = {
            "name": data.get("name"),
            "description": data.get("description")
        }
        update_brand(brand_id, update_data)
        return jsonify({"message": "Brand updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 5. Delete a Brand
@brand_bp.route('/brands/<int:brand_id>', methods=['DELETE'])
def delete_brand_route(brand_id):
    try:
        delete_brand(brand_id)
        return jsonify({"message": "Brand deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 6. Search Products by Brand (New)
@brand_bp.route('/brands/<int:brand_id>/products', methods=['GET'])
def get_products_by_brand(brand_id):
    try:
        # Find the brand by its ID
        brand = get_brand_by_id(brand_id)
        if not brand:
            return jsonify({"error": "Brand not found"}), 404

        brand_name = brand['name']  # Extract the brand name

        # Pagination query parameters
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        skip = (page - 1) * per_page

        # Fetch products by brand name with pagination
        products_cursor = products_collection.find({"brand": brand_name}).skip(skip).limit(per_page)
        products = list(products_cursor)

        # Serialize and return the products
        return jsonify([serialize_product(product) for product in products])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
