import sqlite3
from flask import g
from datetime import datetime
from src.utils import auth

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('database.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def adapt_datetime_iso(val):
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return val.isoformat()

sqlite3.register_adapter(datetime, adapt_datetime_iso)

def convert_datetime(val):
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.fromisoformat(val.decode())

sqlite3.register_converter("datetime", convert_datetime)

class Database:
    def __init__(self, db_path='database.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_if_not_exists()

    def create_if_not_exists(self):
        db = get_db()
        cursor = db.cursor()

        user_table = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """

        product_table = """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE CHECK(LENGTH(nombre) <= 100),
            descripcion TEXT CHECK(LENGTH(descripcion) <= 255),
            cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
            precio INTEGER NOT NULL CHECK(precio >= 0),
            categoria TEXT NOT NULL
        )
        """

        cursor.execute(user_table)
        cursor.execute(product_table)

        db.commit()
    
    def close_connection(self):
        self.conn.close()

    # USER METHODS
    
    def create_user(self, username: str, password: str):
        hashed_password = auth.hash_password(password)
        query = "INSERT INTO usuarios (usuario, password) VALUES (?, ?)"
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (username, hashed_password))
            conn.commit()

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticates a user by verifying the password."""
        query = "SELECT password FROM usuarios WHERE usuario = ?"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        if result:
            stored_password = result[0]
            return auth.verify_password(password, stored_password)
        return False

    # PRODUCT METHODS

    def create_product(self, nombre: str, descripcion: str, cantidad: int, precio: int, categoria: str):
        db = get_db()
        cursor = db.cursor()

        query = """
        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
        VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(query, (nombre, descripcion, cantidad, precio, categoria))
        db.commit()
    
    def get_product_by_id(self, product_id: int):
        query = "SELECT * FROM productos WHERE id = ?"
        self.cursor.execute(query, (product_id,))
        return self.cursor.fetchone()
    
    def get_product_by_name(self, nombre: str):
        query = "SELECT * FROM productos WHERE nombre = ?"
        self.cursor.execute(query, (nombre,))
        return self.cursor.fetchone()
    
    def get_all_products(self):
        query = "SELECT * FROM productos"
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def get_products_by_category(self, categoria: str):
        query = "SELECT * FROM productos WHERE categoria = ?"
        self.cursor.execute(query, (categoria,))
        return self.cursor.fetchall()
    
    def get_out_of_stock_products(self):
        query = "SELECT * FROM productos WHERE cantidad = 0"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_product(self, product_id: int, new_data: dict):
        """
        Updates certain fields of a product with a given ID.

        new_data example:
        ```
        { "nombre": "Gansito", "precio": 800 }
        ```
        """
        set_clause = ', '.join([f"{key} = ?" for key in new_data.keys()])
        values = list(new_data.values())
        values.append(product_id)
        query = f"UPDATE productos SET {set_clause} WHERE id = ?"
        self.cursor.execute(query, values)
        self.conn.commit()
    
    def delete_product(self, product_id: int):
        query = "DELETE FROM productos WHERE id = ?"
        self.cursor.execute(query, (product_id,))
        self.conn.commit()
