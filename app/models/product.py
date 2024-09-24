from bson import ObjectId
from math import ceil

class Product:
    @staticmethod
    def find_all(products_collection):
        return list(products_collection.find())

    @staticmethod
    def find_by_id(products_collection, product_id):
        return products_collection.find_one({"_id": ObjectId(product_id)})

    @staticmethod
    def create(products_collection, product_data):
        result = products_collection.insert_one(product_data)
        return str(result.inserted_id)

    @staticmethod
    def update(products_collection, product_id, product_data):
        products_collection.update_one({"_id": ObjectId(product_id)}, {"$set": product_data})

    @staticmethod
    def delete(products_collection, product_id):
        products_collection.delete_one({"_id": ObjectId(product_id)})

    @staticmethod
    def find_coming_soon(products_collection):
        return list(products_collection.find({"is_coming_soon": True}))
    
    @staticmethod
    def find_latest_product(products_collection):
        return list(products_collection.find({"is_coming_soon": False}))
    
    @staticmethod
    def search(products_collection, query, page, per_page):
        # Tìm kiếm sản phẩm theo tên hoặc mô tả
        search_query = {
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},  # Tìm theo tên, không phân biệt hoa thường
                {"description": {"$regex": query, "$options": "i"}}  # Tìm theo mô tả, không phân biệt hoa thường
            ]
        }
        # Đếm tổng số kết quả
        total_results = products_collection.count_documents(search_query)
        # Sử dụng skip và limit để phân trang
        results = list(products_collection.find(search_query)
                    .skip((page - 1) * per_page)
                    .limit(per_page))
        return results, total_results

    @staticmethod
    def find_paginated(products_collection, page, per_page):
        total = products_collection.count_documents({})
        total_pages = ceil(total / per_page)
        skip = (page - 1) * per_page
        products = list(products_collection.find().skip(skip).limit(per_page))
        return {
            'products': products,
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages
        }