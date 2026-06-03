import sqlite3

DB_NAME = "news.db"

def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS news (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,

        link TEXT,

        date TEXT

    )

    """)

    cursor.execute("PRAGMA table_info(news)")
    columns = [row[1] for row in cursor.fetchall()]
    if "date" not in columns:
        cursor.execute("ALTER TABLE news ADD COLUMN date TEXT")

    conn.commit()

    conn.close()

    print("База данных готова")