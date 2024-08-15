from app import mongo
from bson import ObjectId

class Product:
    @staticmethod
    def find_all():
        return list(mongo.db.products.find())

    @staticmethod
    def find_by_id(product_id):
        return mongo.db.products.find_one({"_id": ObjectId(product_id)})

    @staticmethod
    def create(product_data):
        result = mongo.db.products.insert_one(product_data)
        return str(result.inserted_id)

    @staticmethod
    def update(product_id, product_data):
        mongo.db.products.update_one({"_id": ObjectId(product_id)}, {"$set": product_data})

    @staticmethod
    def delete(product_id):
        mongo.db.products.delete_one({"_id": ObjectId(product_id)})