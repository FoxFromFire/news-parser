import sqlite3

DB_NAME = "news.db"

def save_to_db(data):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    for item in data:

        cursor.execute("""

        INSERT INTO news (title, link)

        VALUES (?, ?)

        """, (

            item["title"],
            item["link"]

        ))

    conn.commit()

    conn.close()

    print("Данные сохранены в БД")