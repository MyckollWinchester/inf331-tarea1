from flask import Flask
from flask_jwt_extended import JWTManager
from src.blueprints.product import product_bp
from src.blueprints.user import user_bp
from src.database import close_db

app = Flask(__name__)

# Configuración de JWT
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # Cambia esto por una clave secreta segura
jwt = JWTManager(app)

# Registrar blueprints
app.register_blueprint(product_bp)
app.register_blueprint(user_bp, url_prefix='/api')

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

if __name__ == '__main__':
    app.run(debug=True)
