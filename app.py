from flask import Flask
from src.routes.product_routes import product_bp
from src.routes.user_routes import user_bp

app = Flask(__name__)

app.register_blueprint(product_bp)
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(debug=True)
