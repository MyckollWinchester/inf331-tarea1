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
        # después hacer un solo submenú para listar productos (2, 3, 4 y 5)
        print("2. Listar productos")
        print("3. Buscar producto por ID")
        print("4. Buscar producto por nombre")
        print("5. Buscar productos por categoría")
        print("6. Listar productos sin stock")
        print("7. Actualizar producto")
        print("8. Eliminar producto")
        print("9. Valor total del inventario")
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
        elif choice == '2':
            response = requests.get(f"{API_URL}/products")
            if response.status_code == 200:
                products = response.json()
                print("Lista de productos:")
                for product in products:
                    print(product)
            else:
                print("Error al obtener la lista de productos.")
        elif choice == '3':
            product_id = int(input("Ingrese el ID del producto: "))
            response = requests.get(f"{API_URL}/products/{product_id}")
            if response.status_code == 200:
                product = response.json()
                print("Producto encontrado:", product)
            else:
                print("Error al obtener el producto.")
        elif choice == '4':
            nombre = input("Ingrese el nombre del producto: ")
            response = requests.get(f"{API_URL}/products/name/{nombre}")
            if response.status_code == 200:
                product = response.json()
                print("Producto encontrado:", product)
            else:
                print("Error al obtener el producto.")
        elif choice == '5':
            categoria = input("Ingrese la categoría del producto: ")
            response = requests.get(f"{API_URL}/products/category/{categoria}")
            if response.status_code == 200:
                products = response.json()
                for product in products:
                    print(product)
                if not products:
                    print("No se encontraron productos en esta categoría.")
            else:
                print("Error al obtener los productos.")
        elif choice == '6':
            response = requests.get(f"{API_URL}/products/out_of_stock")
            if response.status_code == 200:
                products = response.json()
                print("Productos sin stock:")
                for product in products:
                    print(product)
            else:
                print("Error al obtener los productos sin stock.")
        elif choice == '7':
            product_id = int(input("Ingrese el ID del producto a actualizar: "))
            response = requests.get(f"{API_URL}/products/{product_id}")
            if response.status_code != 200:
                print("No se encontró el producto para el ID proporcionado.")
                continue
            product = response.json()
            while True:
                print("Producto actual:", product)

                print("Campos disponibles para actualizar:")
                print("1. Nombre")
                print("2. Descripción")
                print("3. Cantidad")
                print("4. Precio")
                print("5. Categoría")
                print("0. Terminar actualización")

                field_choice = input("Seleccione el campo a actualizar: ")
                if field_choice == '1':
                    product['nombre'] = input("Ingrese el nuevo nombre del producto: ")
                elif field_choice == '2':
                    product['descripcion'] = input("Ingrese la nueva descripción del producto: ")
                elif field_choice == '3':
                    try:
                        new_value = int(input("Ingrese la nueva cantidad del producto: "))
                    except ValueError:
                        print("Error: La cantidad debe ser un número entero.")
                        continue
                    if new_value < 0:
                        print("Error: La cantidad no puede ser negativa.")
                        continue
                    product['cantidad'] = new_value
                elif field_choice == '4':
                    try:
                        new_value = int(input("Ingrese el nuevo precio del producto: "))
                    except ValueError:
                        print("Error: El precio debe ser un número entero.")
                        continue
                    if new_value < 0:
                        print("Error: El precio no puede ser negativo.")
                        continue
                    product['precio'] = new_value
                elif field_choice == '5':
                    product['categoria'] = input("Ingrese la nueva categoría del producto: ")
                elif field_choice == '0':
                    break
                else:
                    print("Opción no válida. Intente nuevamente.")
            response = requests.put(f"{API_URL}/products/{product_id}", json=product)
            if response.status_code == 200:
                print("Producto actualizado exitosamente.")
            else:
                print("Nombre de producto en conflicto con otro existente.")
        elif choice == '8':
            product_id = int(input("Ingrese el ID del producto a eliminar: "))
            response = requests.delete(f"{API_URL}/products/{product_id}")
            if response.status_code == 200:
                print("Producto eliminado exitosamente.")
            else:
                print("Error al eliminar el producto.")
        elif choice == '9':
            response = requests.get(f"{API_URL}/products/inventory_value")
            if response.status_code == 200:
                total_value = response.json().get('total_inventory_value', 0)
                print(f"Valor total del inventario: {total_value}")
            else:
                print("Error al obtener el valor total del inventario.")
        elif choice == '0':
            print("Saliendo del sistema.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == '__main__':
    main()
