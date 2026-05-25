import sqlite3

DB_NAME = "news.db"

def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS news (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,

        link TEXT

    )

    """)

    conn.commit()

    conn.close()

    print("База данных готова")