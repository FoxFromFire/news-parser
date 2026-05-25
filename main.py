from auth import login
import auth
from fetcher import fetch
from database import init_db
from new_parser import parse_news

from saver import save_to_db

from config import BASE_URL


def main():

    init_db()

    success = login()

    if not success:
        return

    role = auth.current_user["role"]

    if role == "viewer":

        url = BASE_URL

    elif role == "operator":

        url = input("Введите URL: ")

    else:

        print("Нет доступа")

        return

    html = fetch(url)

    if not html:

        print("HTML не получен")

        return

    data = parse_news(html)

    print(f"Найдено: {len(data)}")

    save_to_db(data)
if __name__ == "__main__":

    main()