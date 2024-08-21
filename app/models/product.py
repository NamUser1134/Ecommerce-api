from bson import ObjectId

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
