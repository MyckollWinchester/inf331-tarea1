# **Requerimientos Completos - Aplicación de Gestión de Inventario**

## **1. CRUD de Productos**
El sistema debe permitir gestionar productos en una base de datos SQLite con la siguiente estructura:

### **Tabla `productos`**
| Campo        | Tipo      | Restricciones                                |
|-------------|----------|----------------------------------------------|
| `id`        | INTEGER  | Clave primaria, autoincremental              |
| `nombre`    | TEXT     | Obligatorio, máximo 100 caracteres, único     |
| `descripcion` | TEXT   | Opcional, máximo 255 caracteres               |
| `cantidad`  | INTEGER  | Obligatorio, mínimo 0                         |
| `precio`    | REAL     | Obligatorio, mínimo 0.01                      |
| `categoria` | TEXT     | Obligatorio, debe pertenecer a una lista predefinida |

### **Operaciones CRUD**
- **Crear**: Agregar productos con los atributos mencionados.
- **Leer**: Consultar productos por ID, nombre o listar todos.
- **Actualizar**: Modificar cualquier atributo de un producto existente (menos id).
- **Eliminar**: Borrar un producto del inventario.

## **2. Gestión de Stock**
- **Salida de productos**: Reducir stock al vender productos, asegurando que no se venda más de lo disponible.
- **Entrada de productos**: Aumentar la cantidad cuando se reciban nuevas unidades.

## **3. Filtrado y Búsqueda**
- **Buscar productos** por **nombre o ID**.
- **Filtrar productos** por **categoría**.
- **Listar productos agotados** (cantidad en 0).

## **4. Generación de Reportes**
El sistema debe generar los siguientes reportes en consola:
- **Resumen general**: Total de productos en inventario.
- **Valor total del inventario**: Suma de (`cantidad` × `precio`).
- **Lista de productos agotados**.

## **5. Autenticación**
Los usuarios se manejarán en SQLite.

### **Tabla `usuarios`**
| Campo      | Tipo      | Restricciones                              |
|-----------|----------|------------------------------------------|
| `id`      | INTEGER  | Clave primaria, autoincremental         |
| `usuario` | TEXT     | Obligatorio, único                      |
| `password` | TEXT    | Obligatorio, almacenado en hash         |

### **Requisitos de Autenticación**
- Se pedirá **nombre de usuario y contraseña** al inicio.
- Se permitirán **3 intentos** antes de bloquear el acceso temporalmente.
- Contraseñas almacenadas de forma segura con **hashing (`bcrypt`)**.

## **6. Supuestos**
- La aplicación **será solo para un usuario administrador**, sin roles adicionales.
- La conexión a SQLite se hará mediante la librería `sqlite3` en Python.
- La interfaz será **100% en consola (CLI)**.
- No se requiere acceso remoto ni múltiples sesiones concurrentes.
