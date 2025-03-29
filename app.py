import requests

API_URL = "http://127.0.0.1:5000/api"

def main():
    print("Bienvenido al sistema de autenticación.")
    logged_in = False  # Bandera para verificar si el usuario ha iniciado sesión

    while not logged_in:  # Bucle para autenticación y registro
        print("\nOpciones:")
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            username = input("Ingrese un nombre de usuario: ")
            password = input("Ingrese una contraseña: ")
            response = requests.post(f"{API_URL}/users", json={
                "usuario": username,
                "password": password
            })

            if response.status_code == 201:
                print("Usuario registrado exitosamente.")
            else:
                try:
                    error_message = response.json().get('error', 'Error desconocido')
                except requests.exceptions.JSONDecodeError:
                    error_message = "Error desconocido (respuesta no válida del servidor)"
                print(f"Error: {error_message}")
        elif choice == '2':
            username = input("Ingrese su nombre de usuario: ")
            while True:
                password = input("Ingrese su contraseña: ")
                response = requests.post(f"{API_URL}/users/authenticate", json={
                    "usuario": username,
                    "password": password
                })

                if response.status_code == 200:
                    print("Inicio de sesión exitoso.")
                    logged_in = True  # Cambiar la bandera para salir del bucle
                    break
                elif response.status_code == 403:
                    print(response.json().get('error', 'Usuario bloqueado temporalmente. Intente más tarde.'))
                    break
                elif response.status_code == 401:
                    print(response.json().get('error', 'Credenciales incorrectas.'))
                else:
                    print("Error desconocido. Intente nuevamente.")
        elif choice == '3':
            print("Saliendo del sistema.")
            return  # Salir completamente del programa
        else:
            print("Opción no válida. Intente nuevamente.")

    # Segundo bucle: Opciones de productos
    while True:
        print("\nOpciones:")
        print("1. Crear producto")
        print("0. Salir")

        choice = input("Seleccione una opción: ")
        if choice == '1':
            nombre = input("Ingrese el nombre del producto: ")
            descripcion = input("Ingrese la descripción del producto: ")
            cantidad = int(input("Ingrese la cantidad del producto: "))
            precio = float(input("Ingrese el precio del producto: "))
            categoria = input("Ingrese la categoría del producto: ")

            response = requests.post(f"{API_URL}/products", json={
                "nombre": nombre,
                "descripcion": descripcion,
                "cantidad": cantidad,
                "precio": precio,
                "categoria": categoria
            })

            if response.status_code == 201:
                print("Producto creado exitosamente.")
            else:
                print("Error al crear el producto.")

        elif choice == '0':
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == '__main__':
    main()
