from flask import Blueprint, jsonify, request
from src.database import Database

product_bp = Blueprint('products', __name__, url_prefix='/products')

@product_bp.get('/ping')
def ping():
    return jsonify({'message': 'pong'}), 200

@product_bp.post('')
def create_product():
    db = Database()
    product = request.json
    db.create_product(
        nombre=product['nombre'],
        descripcion=product['descripcion'],
        cantidad=product['cantidad'],
        precio=product['precio'],
        categoria=product['categoria']
    )
    return jsonify(product), 201
