import requests

API_URL = "http://127.0.0.1:5000"

def main():
    # user_model = UserModel()
    print("Bienvenido al sistema de autenticación.")
    # while True:
    if False:
        print("\nOpciones:")
        print("1. Registrar nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Salir")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            username = input("Ingrese un nombre de usuario: ")
            password = input("Ingrese una contraseña: ")
            # try:
            #     user_model.create_user(username, password)
            #     print("Usuario registrado exitosamente.")
            # except sqlite3.IntegrityError:
                # print("Error: El nombre de usuario ya existe.")
        elif choice == '2':
            username = input("Ingrese su nombre de usuario: ")
            attempts = 0
            while attempts < 3:
                password = input("Ingrese su contraseña: ")
                # if user_model.authenticate_user(username, password):
                #     print("Inicio de sesión exitoso.")
                #     break
                # else:
                #     attempts += 1
                #     print(f"Contraseña incorrecta. Intentos restantes: {3 - attempts}")
            else:
                print("Demasiados intentos fallidos. Acceso bloqueado temporalmente.")
        elif choice == '3':
            print("Saliendo del sistema.")
            exit()
        else:
            print("Opción no válida. Intente nuevamente.")
    print("Usuario autenticado.")
    
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
