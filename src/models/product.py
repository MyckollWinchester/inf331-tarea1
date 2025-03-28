import sqlite3

class ProductModel:
    def __init__(self, db_path='database.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE CHECK(LENGTH(nombre) <= 100),
            descripcion TEXT CHECK(LENGTH(descripcion) <= 255),
            cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
            precio REAL NOT NULL CHECK(precio >= 0.01),
            categoria TEXT NOT NULL
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def create_product(self, nombre: str, descripcion: str, cantidad: int, precio: float, categoria: str):
        query = """
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (nombre, descripcion, cantidad, precio, categoria))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()