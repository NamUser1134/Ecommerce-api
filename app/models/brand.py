# models/brand.py
from app import brands_collection

class Brand:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

# Functions to interact with MongoDB
def get_all_brands():
    return list(brands_collection.find())

def get_brand_by_id(brand_id):
    brand = brands_collection.find_one({"id": brand_id})
    if brand and '_id' in brand:
        brand['_id'] = str(brand['_id'])
    return brand

def add_brand(brand_data):
    brands_collection.insert_one(brand_data)

def update_brand(brand_id, update_data):
    # Update the brand in MongoDB
    brands_collection.update_one({"id": brand_id}, {"$set": update_data})

def delete_brand(brand_id):
    # The error was likely here with an incomplete string literal.
    brands_collection.delete_one({"id": brand_id})  # Ensure this line is complete
