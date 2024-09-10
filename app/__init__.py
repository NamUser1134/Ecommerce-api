from flask import Flask
from pymongo import MongoClient
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)


# Enable CORS for specific routes and origins
CORS(app, resources={r"/api/*": {"origins": ""}})
# Kết nối tới MongoDB
client = MongoClient("mongodb+srv://namdang3570:minhquy13@cluster0.eafdrjb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['online_shop']

# Khởi tạo collections
categories_collection = db['categories']
products_collection = db['products']

# Import routes AFTER the collections and app are initialized
from app.routes.product_routes import product_bp
from app.routes.category_routes import category_bp

# Register the blueprints
app.register_blueprint(product_bp)
app.register_blueprint(category_bp)
