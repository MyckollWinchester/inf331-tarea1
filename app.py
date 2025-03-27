from flask import Flask, jsonify
from src.routes.product_routes import product_bp

app = Flask(__name__)

app.register_blueprint(product_bp)

@app.get('/ping')
def ping():
    return jsonify({'message': 'pong'})

if __name__ == '__main__':
    app.run(debug=True)
