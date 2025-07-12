import sqlite3
import grape.config as config

def get_connection():
    return sqlite3.connect(config.DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            year INTEGER,
            type TEXT,
            quantity INTEGER,
            price REAL,
            volume_ml INTEGER,
            cellar_slot TEXT,
            purchase_location TEXT,
            is_favorite BOOLEAN DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wine_id INTEGER NOT NULL,
            date DATE DEFAULT CURRENT_DATE,
            people TEXT,
            food TEXT,
            notes TEXT,
            consumed_bottles INTEGER DEFAULT 0,
            FOREIGN KEY (wine_id) REFERENCES wines(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
           CREATE TABLE IF NOT EXISTS regions (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL UNIQUE
           )
       """)

    cursor.execute("""
           CREATE TABLE IF NOT EXISTS departments (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               code TEXT NOT NULL UNIQUE
           )
       """)

    # Insertion auto des régions/départements si vide
    cursor.execute("SELECT COUNT(*) FROM regions")
    if cursor.fetchone()[0] == 0:
        insert_regions_and_departments(cursor)

    conn.commit()
    conn.close()


def make_request(query, params=(), fetch="all"):
    """
    fetch: "all", "one", "none"
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)

    result = None
    if fetch == "all":
        result = cursor.fetchall()
    elif fetch == "one":
        result = cursor.fetchone()

    conn.commit()
    conn.close()
    return result


def insert_regions_and_departments(cursor):
    regions = {
        "Île-de-France": [("Paris", "75"), ("Seine-et-Marne", "77"), ("Yvelines", "78"), ("Essonne", "91"), ("Hauts-de-Seine", "92"), ("Seine-Saint-Denis", "93"), ("Val-de-Marne", "94"), ("Val-d'Oise", "95")],
        "Auvergne-Rhône-Alpes": [("Ain", "01"), ("Allier", "03"), ("Ardèche", "07"), ("Cantal", "15"), ("Drôme", "26"), ("Isère", "38"), ("Loire", "42"), ("Haute-Loire", "43"), ("Puy-de-Dôme", "63"), ("Rhône", "69"), ("Savoie", "73"), ("Haute-Savoie", "74")],
        "Bourgogne-Franche-Comté": [("Côte-d'Or", "21"), ("Doubs", "25"), ("Jura", "39"), ("Nièvre", "58"), ("Haute-Saône", "70"), ("Saône-et-Loire", "71"), ("Yonne", "89"), ("Territoire de Belfort", "90")],
        "Bretagne": [("Côtes-d'Armor", "22"), ("Finistère", "29"), ("Ille-et-Vilaine", "35"), ("Morbihan", "56")],
        "Centre-Val de Loire": [("Cher", "18"), ("Eure-et-Loir", "28"), ("Indre", "36"), ("Indre-et-Loire", "37"), ("Loir-et-Cher", "41"), ("Loiret", "45")],
        "Corse": [("Corse-du-Sud", "2A"), ("Haute-Corse", "2B")],
        "Grand Est": [("Ardennes", "08"), ("Aube", "10"), ("Marne", "51"), ("Haute-Marne", "52"), ("Meurthe-et-Moselle", "54"), ("Meuse", "55"), ("Moselle", "57"), ("Bas-Rhin", "67"), ("Haut-Rhin", "68"), ("Vosges", "88")],
        "Hauts-de-France": [("Aisne", "02"), ("Nord", "59"), ("Oise", "60"), ("Pas-de-Calais", "62"), ("Somme", "80")],
        "Normandie": [("Calvados", "14"), ("Eure", "27"), ("Manche", "50"), ("Orne", "61"), ("Seine-Maritime", "76")],
        "Nouvelle-Aquitaine": [("Charente", "16"), ("Charente-Maritime", "17"), ("Corrèze", "19"), ("Creuse", "23"), ("Dordogne", "24"), ("Gironde", "33"), ("Landes", "40"), ("Lot-et-Garonne", "47"), ("Pyrénées-Atlantiques", "64"), ("Deux-Sèvres", "79"), ("Vienne", "86"), ("Haute-Vienne", "87")],
        "Occitanie": [("Ariège", "09"), ("Aude", "11"), ("Aveyron", "12"), ("Gard", "30"), ("Haute-Garonne", "31"), ("Gers", "32"), ("Hérault", "34"), ("Lot", "46"), ("Lozère", "48"), ("Hautes-Pyrénées", "65"), ("Pyrénées-Orientales", "66"), ("Tarn", "81"), ("Tarn-et-Garonne", "82")],
        "Pays de la Loire": [("Loire-Atlantique", "44"), ("Maine-et-Loire", "49"), ("Mayenne", "53"), ("Sarthe", "72"), ("Vendée", "85")],
        "Provence-Alpes-Côte d'Azur": [("Alpes-de-Haute-Provence", "04"), ("Hautes-Alpes", "05"), ("Alpes-Maritimes", "06"), ("Bouches-du-Rhône", "13"), ("Var", "83"), ("Vaucluse", "84")],
        "DOM-TOM": [("Guadeloupe", "971"), ("Martinique", "972"), ("Guyane", "973"), ("La Réunion", "974"), ("Mayotte", "976")]
    }

    for region_name, departments in regions.items():
        cursor.execute("INSERT INTO regions (name) VALUES (?)", (region_name,))
        for dept_name, dept_code in departments:
            cursor.execute("INSERT INTO departments (name, code) VALUES (?, ?)", (dept_name, dept_code))
