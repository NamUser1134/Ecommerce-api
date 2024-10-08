from flask import Blueprint, jsonify, request
from app.models.product import Product
from app import products_collection
from bson import json_util, ObjectId
import json
from datetime import datetime, timezone

# Tạo Blueprint cho các route liên quan đến sản phẩm
product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Chào mừng đến với API Thương mại điện tử"}), 200

@product_bp.route('/product', methods=['POST'])
def create_product():
    try:
        # Lấy dữ liệu sản phẩm từ request
        product_data = request.json

        # Kiểm tra dữ liệu đầu vào
        if not product_data or not isinstance(product_data, dict):
            return jsonify({"error": "Dữ liệu đầu vào không hợp lệ"}), 400

        # Kiểm tra các trường bắt buộc
        required_fields = ['name', 'price', 'description']
        for field in required_fields:
            if field not in product_data:
                return jsonify({"error": f"Thiếu trường bắt buộc: {field}"}), 400
            
        # Tự động tạo các trường created_at và release_date nếu không được cung cấp
        current_time = datetime.now(timezone.utc)
        product_data['created_at'] = product_data.get('created_at', current_time.isoformat())
        product_data['release_date'] = product_data.get('release_date', current_time.isoformat())

        # Thêm sản phẩm vào cơ sở dữ liệu
        product_id = Product.create(products_collection, product_data)
        
        # Trả về phản hồi với ID của sản phẩm
        return jsonify({"message": "Tạo sản phẩm thành công", "id": product_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/products', methods=['GET'])
def get_products():
    try:
        # Lấy tất cả các sản phẩm từ cơ sở dữ liệu
        products = Product.find_all(products_collection)
        
        # Trả về danh sách sản phẩm dưới dạng JSON
        return json.loads(json_util.dumps(products)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/product/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        # Tìm sản phẩm theo ID
        product = Product.find_by_id(products_collection, product_id)
        
        # Nếu tìm thấy sản phẩm, trả về nó dưới dạng JSON
        if product:
            return json.loads(json_util.dumps(product)), 200
        else:
            return jsonify({"error": "Không tìm thấy sản phẩm"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/product/<product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        # Lấy dữ liệu cập nhật từ request
        product_data = request.json

        # Tự động tạo hoặc cập nhật trường created_at và release_date nếu không được cung cấp
        current_time = datetime.now(timezone.utc)
        product_data['created_at'] = product_data.get('created_at', current_time.isoformat())
        product_data['release_date'] = product_data.get('release_date', current_time.isoformat())

        # Cập nhật sản phẩm trong cơ sở dữ liệu
        Product.update(products_collection, product_id, product_data)
        
        # Trả về thông báo thành công
        return jsonify({"message": "Cập nhật sản phẩm thành công"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        # Xóa sản phẩm theo ID
        Product.delete(products_collection, product_id)
        
        # Trả về thông báo thành công
        return jsonify({"message": "Xóa sản phẩm thành công"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/products/coming-soon', methods=['GET'])
def get_coming_soon_products():
    try:
        # Tìm tất cả các sản phẩm sắp ra mắt
        coming_soon_products = Product.find_coming_soon(products_collection)
        
        # Trả về danh sách sản phẩm dưới dạng JSON
        return json.loads(json_util.dumps(coming_soon_products)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/products/latest', methods=['GET'])
def get_latest_products():
    try:
        # Tìm tất cả các sản phẩm mới nhất
        latest_products = Product.find_latest_product(products_collection)
        
        # Trả về danh sách sản phẩm dưới dạng JSON
        return json.loads(json_util.dumps(latest_products)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/products/search', methods=['GET'])
def search_products():
    try:
        # Lấy các query từ tham số URL
        query = request.args.get('q', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Nếu không có query, trả về lỗi
        if not query:
            return jsonify({"error": "Vui lòng cung cấp từ khóa tìm kiếm"}), 400

        # Tìm kiếm sản phẩm với phân trang
        results, total_results = Product.search(products_collection, query, page, per_page)

        # Trả về kết quả tìm kiếm dưới dạng JSON kèm theo thông tin phân trang
        response = {
            "results": json.loads(json_util.dumps(results)),
            "total_results": total_results,
            "current_page": page,
            "per_page": per_page,
            "total_pages": (total_results + per_page - 1) // per_page  # Tính tổng số trang
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.route('/products/paginated', methods=['GET'])
def get_paginated_products():
    try:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        if page < 1 or per_page < 1:
            return jsonify({"error": "Invalid page or per_page parameters"}), 400

        paginated_result = Product.find_paginated(products_collection, page, per_page)
        
        # Convert ObjectId to string for JSON serialization
        for product in paginated_result['products']:
            product['_id'] = str(product['_id'])

        return jsonify({
            'products': paginated_result['products'],
            'page': paginated_result['page'],
            'per_page': paginated_result['per_page'],
            'total': paginated_result['total'],
            'total_pages': paginated_result['total_pages']
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
