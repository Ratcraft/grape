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
            is_favorite BOOLEAN
        )
    """)
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
