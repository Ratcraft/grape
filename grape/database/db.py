import sqlite3

DB_PATH = "wine_cellar.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            year INTEGER,
            type TEXT,
            quantity INTEGER
        )
    """)
    conn.commit()
    conn.close()
