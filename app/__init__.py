from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

# Kết nối tới MongoDB
client = MongoClient("mongodb+srv://namdang3570:minhquy13@cluster0.eafdrjb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['online_shop']

# Products collection
products_collection = db['products']


# Import routes sau khi đã tạo app
from app.routes import product_routes