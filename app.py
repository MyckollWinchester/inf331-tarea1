from flask import Flask, jsonify
from src.routes.product_routes import product_bp
from src.models.user import UserModel
import sqlite3

app = Flask(__name__)

app.register_blueprint(product_bp)

@app.get('/ping')
def ping():
    return jsonify({'message': 'pong'})

def main():
    user_model = UserModel()
    print("Bienvenido al sistema de autenticación.")
    while True:
        print("\nOpciones:")
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            username = input("Ingrese un nombre de usuario: ")
            password = input("Ingrese una contraseña: ")
            try:
                user_model.create_user(username, password)
                print("Usuario registrado exitosamente.")
            except sqlite3.IntegrityError:
                print("Error: El nombre de usuario ya existe.")
        elif choice == '2':
            username = input("Ingrese su nombre de usuario: ")
            attempts = 0
            while attempts < 3:
                password = input("Ingrese su contraseña: ")
                if user_model.authenticate_user(username, password):
                    print("Inicio de sesión exitoso.")
                    break
                else:
                    attempts += 1
                    print(f"Contraseña incorrecta. Intentos restantes: {3 - attempts}")
            else:
                print("Demasiados intentos fallidos. Acceso bloqueado temporalmente.")
        elif choice == '3':
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

    user_model.close_connection()

if __name__ == '__main__':
    main()
