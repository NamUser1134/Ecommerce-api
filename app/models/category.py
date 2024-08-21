# models/category.py
from app import categories_collection  # Import the initialized collection from the app

class Category:
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
def get_all_categories():
    return list(categories_collection.find())

def get_category_by_id(category_id):
    category = categories_collection.find_one({"id": category_id})
    if category and '_id' in category:
        category['_id'] = str(category['_id'])
    return category

def add_category(category_data):
    categories_collection.insert_one(category_data)

def delete_category(category_id):
    categories_collection.delete_one({"id": category_id})
