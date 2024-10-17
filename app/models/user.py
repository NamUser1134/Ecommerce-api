from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @staticmethod
    def find_by_email(users_collection, email):
        return users_collection.find_one({"email": email})

    @staticmethod
    def find_by_id(users_collection, user_id):
        return users_collection.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def create(users_collection, user_data):
        # Hash the password before storing
        user_data['password'] = generate_password_hash(user_data['password'])
        result = users_collection.insert_one(user_data)
        return str(result.inserted_id)

    @staticmethod
    def update(users_collection, user_id, user_data):
        # If password is in the user_data, hash it before updating
        if 'password' in user_data:
            user_data['password'] = generate_password_hash(user_data['password'])
        
        # Update the user data in the database
        users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": user_data})

    @staticmethod
    def delete(users_collection, user_id):
        users_collection.delete_one({"_id": ObjectId(user_id)})

    @staticmethod
    def check_password(user_data, password):
        return check_password_hash(user_data['password'], password)
