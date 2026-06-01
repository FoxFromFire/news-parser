from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import BASE_URL, BAD_KEYWORDS

DEFAULT_MAX_NEWS = 20
NEXT_PAGE_SELECTORS = [
    "a[rel='next']",
    ".pagination a.next",
    ".pager a.next",
    ".nav-next a",
    ".next-page",
    ".page-next",
    ".pagination__next",
    ".pager__next",
]
NEXT_PAGE_TEXTS = {
    "следующая",
    "следующая страница",
    "next",
    "далее",
    "more",
}


# ---------------- HELPERS ----------------

def clean_text(text):
    return " ".join(text.split())


def normalize_link(href):
    if not href:
        return None
 
    href = href.strip()

    if href.startswith(("javascript:", "#", "mailto:")):
        return None

    link = urljoin(BASE_URL, href)

    # фильтр мусора
    if any(x in link.lower() for x in ["utm_", ".jpg", ".png", ".pdf"]):
        return None

    return link


def is_bad_title(title):
    t = title.lower()
    return any(k in t for k in BAD_KEYWORDS)


def is_bad_url(url):
    return any(x in url.lower() for x in [
        "/tag/", "/category/", "/author/",
        "page=", "search", "login"
    ])


def extract_date(node):
    if node is None:
        return None

    selectors = [
        "time",
        ".date",
        ".news-date",
        ".posted-on",
        ".publish-time",
        ".published",
        ".item-date",
        ".article-date",
        ".date-time",
    ]

    def extract_from(tag):
        if not tag:
            return None
        value = tag.get("datetime") or tag.get_text(strip=True)
        return " ".join(value.split()) if value else None

    candidates = [node]
    if node.parent is not None:
        candidates.append(node.parent)
    parent_article = node.find_parent("article")
    if parent_article is not None:
        candidates.append(parent_article)

    for candidate in candidates:
        for selector in selectors:
            tag = candidate.select_one(selector)
            if tag:
                date_text = extract_from(tag)
                if date_text:
                    return date_text

    return None


def find_next_page_link(html):
    soup = BeautifulSoup(html, "html.parser")
    for selector in NEXT_PAGE_SELECTORS:
        button = soup.select_one(selector)
        if button and button.get("href"):
            next_link = normalize_link(button.get("href"))
            if next_link:
                return next_link

    for a in soup.select("a[href]"):
        text = clean_text(a.get_text(strip=True)).lower()
        if text in NEXT_PAGE_TEXTS:
            next_link = normalize_link(a.get("href"))
            if next_link:
                return next_link

    return None


# ---------------- MAIN PARSER ----------------

def extract_news_items(soup, seen_links):
    news = []

    for card in soup.select("div.main-news_super_item"):
        title_tag = card.select_one(".main-news_super_item_title a")

        if not title_tag:
            continue

        title = clean_text(title_tag.get_text(strip=True))
        link = normalize_link(title_tag.get("href"))

        if not link or link in seen_links:
            continue

        if is_bad_url(link):
            continue

        if len(title.split()) < 3:
            continue

        if is_bad_title(title):
            continue

        date = extract_date(card)
        seen_links.add(link)
        news.append({
            "title": title,
            "link": link,
            "date": date,
        })

    return news


# ---------------- FALLBACK (на всякий случай) ----------------

def fallback_parse(soup, seen_links):
    news = []

    for a in soup.select("article a[href], .news a[href]"):
        title = clean_text(a.get_text(strip=True))
        link = normalize_link(a.get("href"))

        if not link or link in seen_links:
            continue

        if is_bad_url(link):
            continue

        if len(title.split()) < 4:
            continue

        if is_bad_title(title):
            continue

        date = extract_date(a)
        seen_links.add(link)
        news.append({
            "title": title,
            "link": link,
            "date": date,
        })

    return news


# ---------------- ENTRY ----------------

def parse_news(html, seen_links=None, limit=DEFAULT_MAX_NEWS):
    soup = BeautifulSoup(html, "html.parser")

    if seen_links is None:
        seen_links = set()

    # 1. основной парсер (карточки)
    news = extract_news_items(soup, seen_links)

    # 2. fallback только если почти пусто
    if len(news) < 3:
        news.extend(fallback_parse(soup, seen_links))

    # 3. дедупликация
    news = list({item["link"]: item for item in news}.values())

    return news[:limit]