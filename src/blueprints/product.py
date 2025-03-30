from flask import Blueprint, jsonify, request
from src.database import Database

product_bp = Blueprint('products', __name__, url_prefix='/api/products')

@product_bp.post('/')
def create_product():
    db = Database()
    product = request.json
    db.create_product(
        nombre      = product['nombre'],
        descripcion = product['descripcion'],
        cantidad    = product['cantidad'],
        precio      = product['precio'],
        categoria   = product['categoria']
    )
    return jsonify(product), 201

@product_bp.get('/')
def get_all_products():
    db = Database()
    products = db.get_all_products()
    if not products:
        return jsonify({'message': 'No products found'}), 404
    return jsonify(products), 200

@product_bp.get('/<int:product_id>')
def get_product_by_id(product_id):
    db = Database()
    product = db.get_product_by_id(product_id)
    if product:
        return jsonify(product), 200
    return jsonify({'message': 'Product not found'}), 404

@product_bp.get('/name/<string:nombre>')
def get_product_by_name(nombre):
    db = Database()
    product = db.get_product_by_name(nombre)
    if product:
        return jsonify(product), 200
    return jsonify({'message': 'Product not found'}), 404

@product_bp.get('/category/<string:categoria>')
def get_products_by_category(categoria):
    db = Database()
    products = db.get_products_by_category(categoria)
    if products:
        return jsonify(products), 200
    return jsonify({'message': 'No products found in this category'}), 404

@product_bp.get('/out_of_stock')
def get_out_of_stock_products():
    db = Database()
    products = db.get_out_of_stock_products()
    if products:
        return jsonify(products), 200
    return jsonify({'message': 'No out of stock products found'}), 404

@product_bp.get('/inventory_value')
def get_inventory_value():
    db = Database()
    total_value = db.get_inventory_value()
    return jsonify({'total_inventory_value': total_value}), 200

@product_bp.put('/<int:product_id>')
def update_product(product_id):
    db = Database()
    product = request.json
    success = db.update_product(product_id=product_id, new_data=product)
    return jsonify({'message': 'Product updated successfully'}), 200 if success else 400

@product_bp.delete('/<int:product_id>')
def delete_product(product_id):
    db = Database()
    success = db.delete_product(product_id=product_id)
    return jsonify({'message': 'Product deleted successfully'}), 200 if success else 400
