from flask import Flask
from src.blueprints.product import product_bp
# from src.routes.user_routes import user_bp
from src.database import close_db

app = Flask(__name__)

app.register_blueprint(product_bp)
# app.register_blueprint(user_bp)

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

if __name__ == '__main__':
    app.run(debug=True)
