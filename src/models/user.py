import sqlite3
import hashlib

class UserModel:
    def __init__(self, db_path='database.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def hash_password(self, password: str) -> str:
        """Hashes the password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username: str, password: str):
        hashed_password = self.hash_password(password)
        query = "INSERT INTO usuarios (usuario, password) VALUES (?, ?)"
        self.cursor.execute(query, (username, hashed_password))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()