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
    def get_all_regions():
        query = "SELECT id, name FROM regions"
        return make_request(query, fetch="all")

    @staticmethod
    def get_all_departments():
        query = "SELECT id, name, code FROM departments"
        return make_request(query, fetch="all")
