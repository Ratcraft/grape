from grape.database.db import make_request

class Region:
    def __init__(self, name, department_code=None, region_id=None):
        self.id = region_id
        self.name = name
        self.department_code = department_code

    @staticmethod
    def create_region(name):
        query = "INSERT INTO regions (name) VALUES (?)"
        make_request(query, (name,), fetch="none")

    @staticmethod
    def create_department(name, code):
        query = "INSERT INTO departments (name, code) VALUES (?, ?)"
        make_request(query, (name, code), fetch="none")

    @staticmethod
    def get_by_id(region_id):
        query = "SELECT id, name FROM regions WHERE id = ?"
        row = make_request(query, (region_id,), fetch="one")
        if row:
            return Region(row[1], region_id=row[0])
        return None

    @staticmethod
    def get_by_name(name):
        query = "SELECT id, name FROM regions WHERE name = ?"
        row = make_request(query, (name,), fetch="one")
        if row:
            return Region(row[1], region_id=row[0])
        return None

    @staticmethod
    def get_all():
        query = "SELECT id, name FROM regions ORDER BY name"
        rows = make_request(query, fetch="all")
        return [Region(row[1], region_id=row[0]) for row in rows]

