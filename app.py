import requests
from src.utils.logs import logger
from src.utils.interface import *

API_URL = "http://127.0.0.1:5000/api"
TOKEN = None  # Variable global para almacenar el token JWT

def main():
    logger.info("Inicio de la aplicación.")
    print("Bienvenido al sistema de autenticación.")

    while True:
        show_auth_menu()
        choice = input()

        if choice == '1':  # Registrar nuevo usuario
            register_user()
        elif choice == '2':  # Iniciar sesión
            if authenticate_user(): break
        elif choice == '0':  # Salir
            logger.info("El usuario salió del sistema.")
            print("Saliendo del sistema.")
            return
        else:
            logger.warning("Opción no válida seleccionada en el menú de autenticación.")
            print("Opción no válida. Intente nuevamente.")
            continue

    while True:
        show_products_menu()
        choice = input()
        if choice == '1': # Crear producto
            create_product()
        elif choice == '2': # Listar productos
            while True:
                show_product_filtering_menu()
                choice = input()
                if choice == '1': # Todos los productos
                    get_all_products()
                elif choice == '2': # Por ID
                    get_product_by_id()
                elif choice == '3': # Por nombre
                    get_product_by_name()
                elif choice == '4': # Por categoría
                    get_products_by_category()
                elif choice == '0': # Regresar
                    break
                else:
                    logger.warning("Opción no válida seleccionada en el menú de filtrado de productos.")
                    print("Opción no válida. Intente nuevamente.")
                    continue
        elif choice == '3': # Actualizar producto
            update_product()
        elif choice == '4': # Eliminar producto
            delete_product()
        elif choice == '5': # Generar reporte
            while True:
                show_report_menu()
                choice = input()
                if choice == '1': # Resumen general
                    get_general_resume()
                elif choice == '2': # Valor total del inventario
                    get_inventory_value()
                elif choice == '3': # Productos sin existencias
                    get_out_of_stock_products()
                elif choice == '0': # Regresar
                    break
                else:
                    logger.warning("Opción no válida seleccionada en el menú de reporte.")
                    print("Opción no válida. Intente nuevamente.")
        elif choice == '0':
            logger.info("El usuario salió del menú de productos.")
            print("Saliendo del sistema.")
            return
        else:
            logger.warning("Opción no válida seleccionada en el menú de productos.")
            print("Opción no válida. Intente nuevamente.")

# USUARIOS

def register_user():
    username = input("Ingrese un nombre de usuario: ")
    password = input("Ingrese una contraseña: ")
    response = requests.post(f"{API_URL}/users", json={
        "usuario": username,
        "password": password
    })

    if response.status_code == 201:
        logger.info(f"Usuario registrado exitosamente: {username}")
        print("Usuario registrado exitosamente.")
    elif response.status_code == 400:
        logger.warning(f"Nombre {username} ya se encuentra asociado a otro usuario.")
        print("El nombre ya se encuentra asociado a otro usuario.")
    else:
        logger.error("Error del servidor al registrar el usuario.")
        print("Error del servidor al registrar el usuario.")

def authenticate_user() -> bool:
    global TOKEN
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")
    
    response = requests.post(f"{API_URL}/users/authenticate", json={
        "usuario": username,
        "password": password
    })

    if response.status_code == 200:
        data = response.json()
        TOKEN = data["access_token"]  # Guardar el token JWT
        logger.info(f"Inicio de sesión exitoso para el usuario: {username}")
        print("Inicio de sesión exitoso.")
        return True
    elif response.status_code == 400:
        logger.warning(f"Usuario y contraseña son obligatorios.")
        print("Usuario y contraseña son obligatorios.")
        return False
    elif response.status_code == 401:
        logger.warning(f"Credenciales incorrectas para el usuario: {username}")
        print("Credenciales incorrectas.")
        return False
    elif response.status_code == 403:
        logger.warning(f"Usuario bloqueado temporalmente: {username}")
        print("Usuario bloqueado temporalmente. Intente más tarde.")
        return False
    else:
        logger.error(f"Error desconocido al autenticar usuario: {username}")
        print("Error desconocido. Intente nuevamente.")
        return False

# PRODUCTOS

def create_product():
    global TOKEN
    headers = {"Authorization": f"Bearer {TOKEN}"}
    nombre = input("Nombre: ")
    descripcion = input("Descripción: ")
    try:
        cantidad = int(input("Cantidad: "))
    except ValueError:
        print("No se ingresó una cantidad válida. Se asignará 0.")
        cantidad = 0
    if cantidad < 0:
        print("No se ingresó una cantidad válida. Se asignará 0.")
        cantidad = 0
    try:
        precio = int(input("Precio: "))
    except ValueError:
        print("No se ingresó una cantidad válida. Se asignará 0.")
        precio = 0
    if precio < 0:
        print("No se ingresó una cantidad válida. Se asignará 0.")
        precio = 0
    categoria = input("Categoría: ")

    response = requests.post(f"{API_URL}/products", json={
        "nombre": nombre,
        "descripcion": descripcion,
        "cantidad": cantidad,
        "precio": precio,
        "categoria": categoria
    }, headers=headers)

    if response.status_code == 201:
        logger.info(f"Producto creado exitosamente.")
        print("Producto creado exitosamente.")
    else:
        logger.error(f"Error al crear el producto.")
        print("Error al crear el producto.")

def get_all_products():
    response = requests.get(f"{API_URL}/products")
    products: list = []
    if response.status_code == 200:
        products = response.json()
    elif response.status_code == 404:
        logger.info("No hay productos en el inventario.")
        print("No hay productos en el inventario.")
    else:
        logger.error("Error al obtener la lista de productos.")
        print("Error al obtener la lista de productos.")
    if products:
        print("ID. Nombre - Descripción - Cantidad - Precio - Categoría")
        for product in products:
            print(f"{product['id']}. {product['nombre']} - {product['descripcion']} - x{product['cantidad']} unidades - {product['precio']}$ - {product['categoria']}")

def get_product_by_id():
    try:
        product_id = int(input("Ingrese el ID del producto: "))
    except ValueError:
        logger.error("El ID debe ser un número entero.")
        print("Error: El ID debe ser un número entero.")
        return
    response = requests.get(f"{API_URL}/products/{product_id}")
    if response.status_code == 200:
        product = response.json()
        logger.info(f"Producto encontrado: {product}")
        print("Producto encontrado:")
        print(f"{product['id']}. {product['nombre']} - {product['descripcion']} - x{product['cantidad']} unidades - {product['precio']}$ - {product['categoria']}")
    elif response.status_code == 404:
        logger.info("No hay productos con el ID proporcionado.")
        print("No hay productos con el ID proporcionado.")
    else:
        logger.error(f"Error al obtener el producto. ID: {product_id}")
        print("Error al obtener el producto.")

def get_product_by_name():
    nombre = input("Ingrese el nombre del producto: ")
    response = requests.get(f"{API_URL}/products/name/{nombre}")
    if response.status_code == 200:
        product = response.json()
        logger.info(f"Producto encontrado: {product}")
        print(f"{product['id']}. {product['nombre']} - {product['descripcion']} - x{product['cantidad']} unidades - {product['precio']}$ - {product['categoria']}")
    elif response.status_code == 404:
        logger.info("No hay productos con el nombre proporcionado.")
        print("No hay productos con el nombre proporcionado.")
    else:
        logger.error(f"Error al obtener el producto. Nombre: {nombre}")
        print("Error al obtener el producto.")

def get_products_by_category():
    categoria = input("Ingrese la categoría del producto: ")
    response = requests.get(f"{API_URL}/products/category/{categoria}")
    if response.status_code == 200:
        products = response.json()
        logger.info(f"Productos encontrados en la categoría {categoria}: {products}")
        print("Productos encontrados en la categoría:")
        for product in products:
            print(f"{product['id']}. {product['nombre']} - {product['descripcion']} - x{product['cantidad']} unidades - {product['precio']}$ - {product['categoria']}")
    elif response.status_code == 404:
        logger.info("No hay productos en esta categoría.")
        print("No hay productos en esta categoría.")
    else:
        logger.error(f"Error al obtener los productos. Categoría: {categoria}")
        print("Error al obtener los productos.")

def update_product():
    try:
        product_id = int(input("Ingrese el ID del producto a actualizar: "))
    except ValueError:
        logger.error("El ID debe ser un número entero.")
        print("Error: El ID debe ser un número entero.")
        return        
    response = requests.get(f"{API_URL}/products/{product_id}")
    if response.status_code != 200:
        print("No se encontró el producto para el ID proporcionado.")
        return
    product = response.json()
    while True:
        show_product_update_menu()
        choice = input()

        if choice == '1':
            product['nombre'] = input("Ingrese el nuevo nombre del producto: ")
        elif choice == '2':
            product['descripcion'] = input("Ingrese la nueva descripción del producto: ")
        elif choice == '3':
            try:
                new_value = int(input("Ingrese la nueva cantidad del producto: "))
            except ValueError:
                print("Error: La cantidad debe ser un número entero.")
                continue
            if new_value < 0:
                print("Error: La cantidad no puede ser negativa.")
                continue
            product['cantidad'] = new_value
        elif choice == '4':
            try:
                new_value = int(input("Ingrese el nuevo precio del producto: "))
            except ValueError:
                print("Error: El precio debe ser un número entero.")
                continue
            if new_value < 0:
                print("Error: El precio no puede ser negativo.")
                continue
            product['precio'] = new_value
        elif choice == '5':
            product['categoria'] = input("Ingrese la nueva categoría del producto: ")
        elif choice == '0':
            break
        else:
            print("Opción no válida. Intente nuevamente.")

    response = requests.put(f"{API_URL}/products/{product_id}", json=product)
    if response.status_code == 200:
        logger.info("Producto actualizado exitosamente.")
        print("Producto actualizado exitosamente.")
    else:
        logger.error("Error al actualizar el producto.")
        print("Error al actualizar el producto.")

def delete_product():
    try:
        product_id = int(input("Ingrese el ID del producto a eliminar: "))
    except ValueError:
        logger.error("El ID debe ser un número entero.")
        print("Error: El ID debe ser un número entero.")
        return
    response = requests.delete(f"{API_URL}/products/{product_id}")
    if response.status_code == 200:
        logger.info("Producto eliminado exitosamente.")
        print("Producto eliminado exitosamente.")
    else:
        logger.info("No existe un producto con el ID proporcionado.")
        print("No existe un producto con el ID proporcionado.")

def get_general_resume():
    response = requests.get(f"{API_URL}/products")
    if response.status_code == 200:
        products = response.json()
        logger.info("Resumen general de productos:")
        print("Resumen general de productos:")
        _sum = 0
        for product in products:
            _sum += product['cantidad']
            print(f"{product['id']}. {product['nombre']} x{product['cantidad']} unidades")
        print(f"Total de productos en el inventario: {_sum}")
    else:
        logger.error("Error al obtener el resumen general.")
        print("Error al obtener el resumen general.")

def get_inventory_value():
    response = requests.get(f"{API_URL}/products/inventory_value")
    if response.status_code == 200:
        total_value = response.json().get('total_inventory_value', 0)
        logger.info(f"Valor total del inventario: {total_value}$")
        print(f"Valor total del inventario: {total_value}$")
    else:
        logger.error("Error al obtener el valor total del inventario.")
        print("Error al obtener el valor total del inventario.")

def get_out_of_stock_products():
    response = requests.get(f"{API_URL}/products/out_of_stock")
    if response.status_code == 200:
        products = response.json()
        logger.info(f"Productos sin stock: {products}")
        print("Productos sin stock:")
        for product in products:
            print(f"{product['id']}. {product['nombre']} - {product['descripcion']} - SIN STOCK - {product['precio']}$ - {product['categoria']}")
    elif response.status_code == 404:
        logger.info("No hay productos sin stock.")
        print("No hay productos sin stock.")
    else:
        logger.error("Error al obtener los productos sin stock.")
        print("Error al obtener los productos sin stock.")

if __name__ == '__main__':
    main()
