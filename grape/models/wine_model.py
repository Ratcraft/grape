from grape.database.db import make_request

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
        query = """
            INSERT INTO wines (name, year, type, quantity, price, volume_ml, cellar_slot, purchase_location, is_favorite)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            wine.name, wine.year, wine.type, wine.quantity,
            wine.price, wine.volume_ml, wine.cellar_slot,
            wine.purchase_location, int(wine.is_favorite)
        )
        make_request(query, params, fetch="none")

    @staticmethod
    def get_all_wines():
        query = """
            SELECT id, name, year, type, quantity, price, volume_ml, cellar_slot, purchase_location, is_favorite
            FROM wines
        """
        rows = make_request(query, fetch="all")
        return [
            Wine(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], bool(row[9]), wine_id=row[0])
            for row in rows
        ]

    @staticmethod
    def get_wine_by_id(wine_id):
        query = """
            SELECT id, name, year, type, quantity, price, volume_ml, cellar_slot, purchase_location, is_favorite
            FROM wines
            WHERE id = ?
        """
        row = make_request(query, (wine_id,), fetch="one")
        if row:
            return Wine(row[1], row[2], row[3], row[4], row[5], row[6],
                        row[7], row[8], bool(row[9]), wine_id=row[0])
        return None

    @staticmethod
    def update_wine(wine_id, name, year, wine_type, quantity, price, volume_ml, cellar_slot, purchase_location):
        query = """
            UPDATE wines
            SET name = ?, year = ?, type = ?, quantity = ?, price = ?, volume_ml = ?, cellar_slot = ?, purchase_location = ?
            WHERE id = ?
        """
        params = (name, year, wine_type, quantity, price, volume_ml, cellar_slot, purchase_location, wine_id)
        make_request(query, params, fetch="none")

    @staticmethod
    def delete_wine(wine_id):
        query = "DELETE FROM wines WHERE id = ?"
        make_request(query, (wine_id,), fetch="none")

    @staticmethod
    def get_all_wines_filtered(name=None, min_quantity=None, year=None):
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

        query += " ORDER BY is_favorite DESC, name ASC"

        rows = make_request(query, tuple(params), fetch="all")

        return [
            Wine(row[1], row[2], row[3], row[4], row[5], row[6],
                 row[7], row[8], bool(row[9]), wine_id=row[0])
            for row in rows
        ]

    def save(self):
        query = """
                UPDATE wines
                SET name              = ?, \
                    year              = ?, \
                    type              = ?, \
                    quantity          = ?, \
                    price             = ?, \
                    volume_ml         = ?, \
                    cellar_slot       = ?, \
                    purchase_location = ?,
                    is_favorite       = ?
                WHERE id = ? \
                """
        params = (self.name, self.year, self.type, self.quantity, self.price,
                  self.volume_ml, self.cellar_slot, self.purchase_location, int(self.is_favorite), self.id)
        make_request(query, params, fetch="none")

    def toggle_favorite(self):
        self.is_favorite = not self.is_favorite
        query = "UPDATE wines SET is_favorite = ? WHERE id = ?"
        make_request(query, (int(self.is_favorite), self.id), fetch="none")
