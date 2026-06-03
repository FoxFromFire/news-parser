import csv
import sqlite3

DB_NAME = "news.db"

def save_to_db(data):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    for item in data:
        cursor.execute("""

        INSERT INTO news (title, link, date)

        VALUES (?, ?, ?)

        """, (
            item.get("title"),
            item.get("link"),
            item.get("date"),
        ))

    conn.commit()

    conn.close()

    print("Данные сохранены в БД")


def save_to_csv(data, filename="news.csv"):
    with open(filename, "w", newline="", encoding="utf-8-sig") as csvfile:
        fieldnames = ["title", "link", "date"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for item in data:
            writer.writerow({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "date": item.get("date", ""),
            })

    print(f"Данные экспортированы в CSV: {filename}")


def save_to_excel(data, filename="news.xlsx"):
    try:
        from openpyxl import Workbook
    except ImportError:
        print("Для экспорта в Excel установите openpyxl")
        return

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "News"

    headers = ["title", "link", "date"]
    worksheet.append(headers)

    for item in data:
        worksheet.append([
            item.get("title", ""),
            item.get("link", ""),
            item.get("date", ""),
        ])

    for index, _ in enumerate(headers, start=1):
        worksheet.column_dimensions[worksheet.cell(row=1, column=index).column_letter].width = 30

    workbook.save(filename)
    print(f"Данные экспортированы в Excel: {filename}")