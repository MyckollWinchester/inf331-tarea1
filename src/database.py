import sqlite3
import json
from datetime import datetime

def adapt_datetime_iso(val):
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return val.isoformat()

sqlite3.register_adapter(datetime, adapt_datetime_iso)

def convert_datetime(val):
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.fromisoformat(val.decode())

sqlite3.register_converter("datetime", convert_datetime)

class database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()

        self.create_if_not_exists()

    def create_if_not_exists(self):
        # Existing tables
        u_table = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            created_at DATE,
            stats TEXT
        )"""
        
        r_table = """
        CREATE TABLE IF NOT EXISTS rolls (
            roll_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            roll_date DATE,
            rolled_students TEXT,

            CONSTRAINT fk_user_id_rolls
            FOREIGN KEY (user_id)
            REFERENCES users(user_id)
        )    
        """

        s_table = """
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            info TEXT
        )"""

        us_table = """
        CREATE TABLE IF NOT EXISTS user_students (
            student_id INTEGER,
            user_id INTEGER,
            stats TEXT,

            CONSTRAINT fk_student_id_user_students
            FOREIGN KEY (student_id)
            REFERENCES students(student_id),

            CONSTRAINT fk_user_id_user_students
            FOREIGN KEY (user_id)
            REFERENCES users(user_id)
        )"""

        # New tables
        usuarios_table = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        """

        productos_table = """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE CHECK(LENGTH(nombre) <= 100),
            descripcion TEXT CHECK(LENGTH(descripcion) <= 255),
            cantidad INTEGER NOT NULL CHECK(cantidad >= 0),
            precio REAL NOT NULL CHECK(precio >= 0.01),
            categoria TEXT NOT NULL
        )
        """

        # Execute table creation
        self.cursor.execute(u_table)
        self.cursor.execute(r_table)
        self.cursor.execute(s_table)
        self.cursor.execute(us_table)
        self.cursor.execute(usuarios_table)
        self.cursor.execute(productos_table)

        self.conn.commit()

    def create_user(self, user_id: int):
        """
        Creates a new user in the database.
        
        Args:
            user_id (int): The discord user id
        """
        with open("static/default_user_stats.json", "r") as file:
            stats = json.load(file)
        self.cursor.execute("INSERT INTO users (user_id, created_at, stats) VALUES (?, ?, ?)", (user_id, datetime.today(), json.dumps(stats)))
        self.conn.commit()
    
    def create_roll(self, user_id: int, roll: list):
        roll = {str(i): roll[i] for i in range(10)}
        self.cursor.execute("INSERT INTO rolls (user_id, roll_date, rolled_students) VALUES (?, ?, ?)", (user_id, datetime.today(), f'{roll}'))
        self.conn.commit()

    def create_student(self, student_name: str, info: dict):
        self.cursor.execute("INSERT INTO students (student_name, info) VALUES (?, ?)", (student_name, json.dumps(info)))
        self.conn.commit()

    def update_student_info(self, student_id: int, info: dict):
        self.cursor.execute("UPDATE students SET info=? WHERE student_id=?", (json.dumps(info), student_id))
        self.conn.commit()

    def get_all_students(self) -> dict[str, dict]:
        self.cursor.execute("SELECT student_id, student_name, info FROM students")
        students = self.cursor.fetchall()
        return {s[0]: json.loads(s[2]) for s in students}

    def get_user_info(self, user_id: int) -> tuple:
        """
        Returns a tuple containing the user creation date and the stats.

        Args:
            user_id (int): The user id to get the stats from.
        """
        self.cursor.execute("SELECT created_at, stats FROM users WHERE user_id=?", (user_id,))
        return self.cursor.fetchone()

    def add_user_student(self, user_id: int, student_id: int):
        self.cursor.execute("INSERT INTO user_students (user_id, student_id, stats) VALUES (?, ?, ?)", (user_id, student_id, json.dumps({})))
        self.conn.commit()

    def get_user_students(self, user_id: int) -> list[int]:
        """
        Returns a list of student ids that the user has.

        Args:
            user_id (int): The user id to get the students from.
        """
        self.cursor.execute("SELECT student_id FROM user_students WHERE user_id=?", (user_id,))
        return [s[0] for s in self.cursor.fetchall()]

    def get_user_rolls(self, user_id: int) -> list[tuple]:
        """
        Returns a list of tuples containing the roll date and the rolled students.

        Args:
            user_id (int): The user id to get the rolls from.
        """
        self.cursor.execute("SELECT roll_date, rolled_students FROM rolls WHERE user_id=?", (user_id,))
        return self.cursor.fetchall()

    def is_user_created(self, user_id: int) -> bool:
        self.cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
        return self.cursor.fetchone() is not None    
    
    def update_user_stats(self, user_id: int, stats: dict):
        self.cursor.execute("UPDATE users SET stats=? WHERE user_id=?", (json.dumps(stats), user_id))
        self.conn.commit()
    
    def reset_daily_roll(self):
        self.cursor.execute("SELECT user_id, stats FROM users")
        users = self.cursor.fetchall()

        for user in users:
            user_id, stats = user
            stats = json.loads(stats)

            stats["daily_free_roll_used"] = False
            self.cursor.execute("UPDATE users SET stats=? WHERE user_id=?", (json.dumps(stats), user_id))

        self.conn.commit()

    def close_connection(self):
        self.conn.close()


if __name__ == "__main__":
    db = database()
    db.close_connection()