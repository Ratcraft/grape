from grape.database.db import make_request
from grape.models.region import Region

class Wine:
    def __init__(self, name, year, wine_type, quantity, price=None, volume_ml=None, cellar_slot=None,
                 purchase_location=None, is_favorite=False, medals=None, expiration_date=None,
                 region=None, wine_id=None):
        self.id = wine_id
        self.name = name
        self.year = year
        self.type = wine_type
        self.quantity = quantity
        self.price = price
        self.volume_ml = volume_ml
        self.cellar_slot = cellar_slot
        self.purchase_location = purchase_location
        self.is_favorite = is_favorite
        self.medals = medals
        self.expiration_date = expiration_date
        self.region = region  # region is an instance of Region

    @staticmethod
    def add_wine(wine):
        query = """
                INSERT INTO wines (name, year, type, quantity, price, volume_ml, cellar_slot, purchase_location,
                                   is_favorite, medals, expiration_date, region_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
        params = (
            wine.name, wine.year, wine.type, wine.quantity,
            wine.price, wine.volume_ml, wine.cellar_slot,
            wine.purchase_location, int(wine.is_favorite),
            wine.medals, wine.expiration_date, wine.region.id if wine.region else None
        )
        make_request(query, params, fetch="none")

    @staticmethod
    def get_all_wines():
        query = """
            SELECT w.id, w.name, w.year, w.type, w.quantity, w.price, w.volume_ml, w.cellar_slot,
                   w.purchase_location, w.is_favorite, w.medals, w.expiration_date, r.id, r.name
            FROM wines w
            LEFT JOIN regions r ON w.region_id = r.id
        """
        rows = make_request(query, fetch="all")
        return [
            Wine(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                 bool(row[9]), medals=row[10], expiration_date=row[11],
                 region=Region(row[13], region_id=row[12]) if row[12] else None, wine_id=row[0])
            for row in rows
        ]

    @staticmethod
    def get_wine_by_id(wine_id):
        query = """
            SELECT w.id, w.name, w.year, w.type, w.quantity, w.price, w.volume_ml, w.cellar_slot,
                   w.purchase_location, w.is_favorite, w.medals, w.expiration_date, r.id, r.name
            FROM wines w
            LEFT JOIN regions r ON w.region_id = r.id
            WHERE w.id = ?
        """
        row = make_request(query, (wine_id,), fetch="one")
        if row:
            return Wine(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8],
                        bool(row[9]), medals=row[10], expiration_date=row[11],
                        region=Region(row[13], region_id=row[12]) if row[12] else None, wine_id=row[0])
        return None

    @staticmethod
    def update_wine(wine_id, name, year, wine_type, quantity, price, volume_ml, cellar_slot,
                    purchase_location, is_favorite, medals, expiration_date, region_id):
        query = """
            UPDATE wines
            SET name = ?, year = ?, type = ?, quantity = ?, price = ?, volume_ml = ?, cellar_slot = ?,
                purchase_location = ?, is_favorite = ?, medals = ?, expiration_date = ?, region_id = ?
            WHERE id = ?
        """
        params = (name, year, wine_type, quantity, price, volume_ml, cellar_slot,
                  purchase_location, int(is_favorite), medals, expiration_date, region_id, wine_id)
        make_request(query, params, fetch="none")

    def save(self):
        Wine.update_wine(
            self.id, self.name, self.year, self.type, self.quantity, self.price,
            self.volume_ml, self.cellar_slot, self.purchase_location,
            self.is_favorite, self.medals, self.expiration_date,
            self.region.id if self.region else None
        )

    @staticmethod
    def delete_wine(wine_id):
        query = "DELETE FROM wines WHERE id = ?"
        make_request(query, (wine_id,), fetch="none")

    @staticmethod
    def get_all_wines_filtered(name=None, min_quantity=None, year=None, region_id=None):
        query = """
            SELECT w.id, w.name, w.year, w.type, w.quantity, w.price, w.volume_ml, w.cellar_slot,
                   w.purchase_location, w.is_favorite, w.medals, w.expiration_date, r.id, r.name
            FROM wines w
            LEFT JOIN regions r ON w.region_id = r.id
            WHERE 1=1
        """
        params = []

        if name:
            query += " AND w.name LIKE ?"
            params.append(f"%{name}%")
        if min_quantity:
            query += " AND w.quantity >= ?"
            params.append(min_quantity)
        if year:
            query += " AND w.year = ?"
            params.append(year)
        if region_id:
            query += " AND w.region_id = ?"
            params.append(region_id)

        query += " ORDER BY w.is_favorite DESC, w.name ASC"

        rows = make_request(query, tuple(params), fetch="all")

        return [
            Wine(row[1], row[2], row[3], row[4], price=row[5], volume_ml=row[6],
                 cellar_slot=row[7], purchase_location=row[8], is_favorite=bool(row[9]),
                 medals=row[10], expiration_date=row[11],
                 region=Region(row[13], region_id=row[12]) if row[12] else None, wine_id=row[0])
            for row in rows
        ]

    def toggle_favorite(self):
        self.is_favorite = not self.is_favorite
        query = "UPDATE wines SET is_favorite = ? WHERE id = ?"
        make_request(query, (int(self.is_favorite), self.id), fetch="none")
