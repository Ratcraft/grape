from grape.database.db import get_connection

class Wine:
    def __init__(self, name, year, type, quantity, price=None, volume_ml=None, cellar_slot=None,
                 purchase_location=None, is_favorite=False, wine_id=None):
        self.id = wine_id
        self.name = name
        self.year = year
        self.type = type
        self.quantity = quantity
        self.price = price
        self.volume_ml = volume_ml
        self.cellar_slot = cellar_slot
        self.purchase_location = purchase_location
        self.is_favorite = is_favorite

    @staticmethod
    def add_wine(wine):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO wines (name, year, type, quantity, price, volume_ml, cellar_slot, purchase_location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            wine.name, wine.year, wine.type, wine.quantity,
            wine.price, wine.volume_ml, wine.cellar_slot, wine.purchase_location
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_wines():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, year, type, quantity, price, volume_ml, cellar_slot, purchase_location, is_favorite
            FROM wines
        """)
        rows = cursor.fetchall()
        conn.close()
        return [
            Wine(row[1], row[2], row[3], row[4], price=row[5], volume_ml=row[6],
                 cellar_slot=row[7], purchase_location=row[8], wine_id=row[0])
            for row in rows
        ]

    @staticmethod
    def get_wine_by_id(wine_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, year, type, quantity, price, volume_ml, cellar_slot, purchase_location, is_favorite
            FROM wines
            WHERE id = ?
        """, (wine_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Wine(row[1], row[2], row[3], row[4], price=row[5], volume_ml=row[6],
                        cellar_slot=row[7], purchase_location=row[8], wine_id=row[0])
        return None

    @staticmethod
    def update_wine(wine_id, name, year, wine_type, quantity, price, volume_ml, cellar_slot, purchase_location):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE wines
            SET name = ?, year = ?, type = ?, quantity = ?, price = ?, volume_ml = ?, cellar_slot = ?, purchase_location = ?,
                is_favorite = ?
            WHERE id = ?
        """, (name, year, wine_type, quantity, price, volume_ml, cellar_slot, purchase_location, wine_id))
        conn.commit()
        conn.close()

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE wines
            SET name = ?, year = ?, type = ?, quantity = ?, price = ?, volume_ml = ?, cellar_slot = ?, purchase_location = ?,
                is_favorite = ?
            WHERE id = ?
        """, (self.name, self.year, self.type, self.quantity, self.price,
              self.volume_ml, self.cellar_slot, self.purchase_location, self.id))
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
    def get_all_wines_filtered(name=None, min_quantity=None, year=None):
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT id, name, year, type, quantity, price, volume_ml, cellar_slot, purchase_location, is_favorite
            FROM wines WHERE 1=1
        """
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

        # Ajout du tri par favoris d'abord
        query += " ORDER BY is_favorite DESC, name ASC"

        cursor.execute(query, tuple(params))
        rows = cursor.fetchall()
        conn.close()

        return [
            Wine(row[1], row[2], row[3], row[4], price=row[5], volume_ml=row[6],
                 cellar_slot=row[7], purchase_location=row[8], wine_id=row[0])
            for row in rows
        ]

    def toggle_favorite(self):
        self.is_favorite = not self.is_favorite
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE wines SET is_favorite = ? WHERE id = ?", (int(self.is_favorite), self.id))
        conn.commit()
        conn.close()

