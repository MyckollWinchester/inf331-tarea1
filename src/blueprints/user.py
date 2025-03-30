from flask import Blueprint, request, jsonify
from src.database import Database
from datetime import datetime, timedelta
from sqlite3 import IntegrityError

user_bp = Blueprint('user_bp', __name__)

# Diccionario para rastrear intentos fallidos y bloqueos temporales
login_attempts = {}

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Endpoint para registrar un nuevo usuario."""
    db = Database()
    data = request.get_json()
    username = data.get('usuario')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Usuario y contraseña son obligatorios"}), 400

    try:
        db.create_user(username, password)
        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    except IntegrityError:
        return jsonify({"error": "El nombre de usuario ya existe. Por favor, elija otro."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/users/authenticate', methods=['POST'])
def authenticate_user():
    """Endpoint para autenticar un usuario."""
    db = Database()
    data = request.get_json()
    username = data.get('usuario')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Usuario y contraseña son obligatorios"}), 400

    # Verificar si el usuario está bloqueado
    if username in login_attempts:
        _, block_time = login_attempts[username]
        if block_time and datetime.now() < block_time:
            return jsonify({"error": "Usuario bloqueado temporalmente. Intente más tarde."}), 403

    # Intentar autenticar al usuario
    if db.authenticate_user(username, password):
        # Restablecer intentos fallidos en caso de éxito
        if username in login_attempts:
            del login_attempts[username]
        return jsonify({"message": "Inicio de sesión exitoso"}), 200
    else:
        # Incrementar intentos fallidos
        if username not in login_attempts:
            login_attempts[username] = [1, None]  # [intentos, tiempo de bloqueo]
        else:
            login_attempts[username][0] += 1

        # Bloquear usuario después de 3 intentos fallidos
        if login_attempts[username][0] >= 3:
            login_attempts[username][1] = datetime.now() + timedelta(minutes=5)  # Bloqueo de 5 minutos
            return jsonify({"error": "Demasiados intentos fallidos. Usuario bloqueado temporalmente."}), 403

        # Informar intentos restantes
        remaining_attempts = 3 - login_attempts[username][0]
        return jsonify({"error": f"Credenciales incorrectas. Intentos restantes: {remaining_attempts}"}), 401