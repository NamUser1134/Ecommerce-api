import os
from bson import ObjectId
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads/images'

class Image:
    @staticmethod
    def save_image(image_file):
        # Secure the filename
        filename = secure_filename(image_file.filename)

        # Save the image to the uploads folder
        image_path = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(image_path)

        # Return the relative path
        return image_path

    @staticmethod
    def create(images_collection, image_data, image_file):
        # Save the image to disk
        image_path = Image.save_image(image_file)

        # Store the image path in the database
        image_data['image_path'] = image_path
        result = images_collection.insert_one(image_data)
        return str(result.inserted_id)
    
    @staticmethod
    def update(images_collection, image_id, image_file):
        # Save the updated image to disk
        image_path = Image.save_image(image_file)
        
        # Update the image path in the database
        images_collection.update_one({"_id": ObjectId(image_id)}, {"$set": {"image_path": image_path}})
    
    @staticmethod
    def delete(images_collection, image_id):
        images_collection.delete_one({"_id": ObjectId(image_id)})
