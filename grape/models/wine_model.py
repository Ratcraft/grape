from grape.database.db import get_connection

class Wine:
    def __init__(self, name, year, type, quantity, wine_id=None):
        self.id = wine_id
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
        conn.close()

    @staticmethod
    def get_all_wines():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, year, type, quantity FROM wines")
        rows = cursor.fetchall()
        conn.close()
        return [Wine(name, year, wine_type, quantity, wine_id=id) for id, name, year, wine_type, quantity in rows]

    @staticmethod
    def get_wine_by_id(wine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, year, type, quantity FROM wines WHERE id = ?", (wine_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Wine(row[1], row[2], row[3], row[4], wine_id=row[0])
        return None

    @staticmethod
    def update_wine(wine_id, name, year, wine_type, quantity):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE wines
                       SET name     = ?, year     = ?, type     = ?, quantity = ?
                       WHERE id = ?
                       """, (name, year, wine_type, quantity, wine_id))
        conn.commit()
        conn.close()

    @staticmethod
    def delete_wine(wine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM wines WHERE id = ?", (wine_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_wines_filtered(name, min_quantity, year):
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT id, name, year, type, quantity FROM wines WHERE 1=1"
        params = []

        if name:
            query += " AND name LIKE ?"
            params.append(f"%{name}%")

        if min_quantity:
            query += " AND quantity >= ?"
            params.append(min_quantity)

        if year:
            query += " AND year = ?"
            params.append(year)

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        conn.close()

        return [Wine(row[1], row[2], row[3], row[4], wine_id=row[0]) for row in rows]


