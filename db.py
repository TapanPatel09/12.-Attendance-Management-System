# # db.py
# import mysql.connector
# from mysql.connector import Error
# from typing import Optional, List, Dict
# import os

# DB_CONFIG = {
#     'host': os.getenv('DB_HOST', 'localhost'),
#     'user': os.getenv('DB_USER', 'root'),
#     'password': os.getenv('DB_PASS', '1234'),
#     'database': os.getenv('DB_NAME', 'attendance_db'),
#     'port': int(os.getenv('DB_PORT', 3306))
# }

# class DB:
#     def __init__(self, config=DB_CONFIG):
#         self.config = config
#         self.conn = None

#     def connect(self):
#         if self.conn and self.conn.is_connected():
#             return self.conn
#         try:
#             self.conn = mysql.connector.connect(**self.config)
#             return self.conn
#         except Error as e:
#             raise RuntimeError(f"DB connection failed: {e}")

#     def execute(self, query: str, params: tuple = ()):
#         conn = self.connect()
#         cursor = conn.cursor(dictionary=True)
#         try:
#             cursor.execute(query, params)
#             conn.commit()
#             return cursor
#         except Error as e:
#             conn.rollback()
#             raise

#     def fetchall(self, query: str, params: tuple = ()):
#         cursor = self.execute(query, params)
#         return cursor.fetchall()

#     def fetchone(self, query: str, params: tuple = ()):
#         cursor = self.execute(query, params)
#         return cursor.fetchone()


import mysql.connector

class Database:
    def __init__(self):
        self.config = {
            "host": "localhost",
            "user": "root",
            "password": "1234",  # 👈 put your MySQL password here
            "database": "attendance_db"
        }
        self.conn = None
        self.ensure_tables()

    def connect(self):
        if not self.conn or not self.conn.is_connected():
            self.conn = mysql.connector.connect(**self.config)
        return self.conn

    def execute(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        conn.commit()
        cursor.close()
        return True

    def fetchall(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        cursor.close()
        return result

    # 👇 This will auto-create the tables if missing
    def ensure_tables(self):
        conn = mysql.connector.connect(
            host=self.config["host"],
            user=self.config["user"],
            password=self.config["password"]
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS attendance_db")
        cursor.close()
        conn.close()

        conn = self.connect()
        cursor = conn.cursor()

        # Students Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            roll VARCHAR(20) PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            class_name VARCHAR(20),
            section VARCHAR(10)
        )
        """)

        # Attendance Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            roll VARCHAR(20),
            date DATE,
            status ENUM('Present','Absent') DEFAULT 'Present',
            FOREIGN KEY (roll) REFERENCES students(roll) ON DELETE CASCADE
        )
        """)

        conn.commit()
        cursor.close()
