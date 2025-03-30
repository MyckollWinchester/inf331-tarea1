def show_menu(options: list, title: str, exit: str = 'Salir'):
    print(f"\n{title}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    if exit:
        print(f"0. {exit}")
    print("\nSeleccione una opción:", end=' ')

# Productos
def show_products_menu():
    title = "Gestor de Productos"
    options = ["Crear producto", "Listar productos", "Actualizar producto", "Eliminar producto", "Generar reporte"]
    show_menu(options, title)

def show_product_filtering_menu():
    title = "Filtrar por"
    options = ["Todos los productos", "Por ID", "Por nombre", "Por categoría"]
    show_menu(options, title)

def show_report_menu():
    title = "Generar Reporte"
    options = ["Resumen general", "Valor total del inventario", "Productos sin existencias"]
    show_menu(options, title)

def show_product_update_menu():
    title = "Actualizar Producto"
    options = ["Nombre", "Descripción", "Cantidad", "Precio", "Categoría"]
    exit_option = "Finalizar actualización"
    show_menu(options, title, exit_option)
