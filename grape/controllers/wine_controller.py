from models.wine_model import Wine

def add_new_wine(name, year, type, quantity):
    wine = Wine(name, int(year), type, int(quantity))
    Wine.add_wine(wine)

def get_all_wines():
    return Wine.get_all_wines()
