from auth import login
import auth
from fetcher import fetch
from database import init_db
from new_parser import find_next_page_link, parse_news
from saver import save_to_csv, save_to_db, save_to_excel
from config import BASE_URL, CSV_FILE, EXCEL_FILE, MAX_PAGES


def collect_news(start_url, max_pages):
    current_url = start_url
    all_news = []
    seen_links = set()

    for page_number in range(1, max_pages + 1):
        print(f"Парсинг страницы {page_number}: {current_url}")
        html = fetch(current_url)

        if not html:
            print("Не удалось получить HTML страницы")
            break

        page_news = parse_news(html, seen_links=seen_links)
        all_news.extend(page_news)

        next_page = find_next_page_link(html)
        if not next_page:
            print("Следующая страница не найдена")
            break

        current_url = next_page

    return all_news


def main():
    init_db()

    success = login()
    if not success:
        return

    role = auth.current_user["role"]

    if role == "viewer":
        url = BASE_URL
        pages = MAX_PAGES
    elif role == "operator":
        url = input("Введите URL: ")
        try:
            pages = int(input(f"Сколько страниц парсить (1-{MAX_PAGES})? ") or 1)
        except ValueError:
            pages = 1
        pages = max(1, min(pages, MAX_PAGES))
    else:
        print("Нет доступа")
        return

    news = collect_news(url, pages)

    if not news:
        print("Данные не найдены")
        return

    print(f"Найдено всего: {len(news)}")

    save_to_db(news)
    save_to_csv(news, CSV_FILE)
    save_to_excel(news, EXCEL_FILE)


if __name__ == "__main__":
    main()