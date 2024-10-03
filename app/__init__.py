from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for the entire app
CORS(app)


# JWT configuration
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a strong secret key
jwt = JWTManager(app)

# Kết nối tới MongoDB
client = MongoClient("mongodb+srv://namdang3570:minhquy13@cluster0.eafdrjb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['online_shop']

# Khởi tạo collections
categories_collection = db['categories']
products_collection = db['products']
brands_collection = db['brands']  # Add this line to initialize the brands collection


# Import routes AFTER the collections and app are initialized
from app.routes.product_routes import product_bp
from app.routes.category_routes import category_bp
from app.routes.brand_routes import brand_bp  # New line for brands

# Register the blueprints
app.register_blueprint(product_bp)
app.register_blueprint(category_bp)
app.register_blueprint(brand_bp)  # New line for registering the brands blueprint
