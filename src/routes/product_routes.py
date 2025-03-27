from flask import Blueprint, jsonify, request

product_bp = Blueprint('product', __name__)

# In-memory storage for products (for demonstration purposes)
products = []

@product_bp.get('/products/ping')
def ping():
    return jsonify({'message': 'pong'})

@product_bp.post('/products')
def create_product():
    product = request.json
    products.append(product)
    return jsonify(product), 201

@product_bp.get('/products')
def get_products():
    return jsonify(products), 200

@product_bp.get('/products/<int:product_id>')
def get_product(product_id):
    if 0 <= product_id < len(products):
        return jsonify(products[product_id]), 200
    return jsonify({'error': 'Product not found'}), 404

@product_bp.put('/products/<int:product_id>')
def update_product(product_id):
    if 0 <= product_id < len(products):
        product = request.json
        products[product_id] = product
        return jsonify(product), 200
    return jsonify({'error': 'Product not found'}), 404

@product_bp.delete('/products/<int:product_id>')
def delete_product(product_id):
    if 0 <= product_id < len(products):
        products.pop(product_id)
        return jsonify({'message': 'Product deleted'}), 204
    return jsonify({'error': 'Product not found'}), 404
