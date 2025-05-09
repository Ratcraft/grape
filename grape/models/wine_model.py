import sqlite3
from database.db import get_connection

class Wine:
    def __init__(self, name, year, type, quantity):
        self.name = name
        self.year = year
        self.type = type
        self.quantity = quantity

    @staticmethod
    def add_wine(wine):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO wines (name, year, type, quantity) VALUES (?, ?, ?, ?)",
                       (wine.name, wine.year, wine.type, wine.quantity))
        conn.commit()

    @staticmethod
    def get_all_wines():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, year, type, quantity FROM wines")
        return cursor.fetchall()
