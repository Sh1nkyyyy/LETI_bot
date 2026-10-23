import html
import re
from bs4 import BeautifulSoup


def clean_lk_html_for_telegram(raw_html: str) -> str:
    if not raw_html:
        return ""

    soup = BeautifulSoup(raw_html, "html.parser")

    # 1. Заменяем <img> с эмодзи на их текстовый эквивалент из alt
    # <img src="..." alt="💙"> -> 💙
    for img in soup.find_all("img"):
        alt_text = img.get("alt", "")
        img.replace_with(alt_text)

    # 2. Нормализуем теги форматирования к разрешенным Telegram
    # strong -> b
    for tag in soup.find_all("strong"):
        tag.name = "b"

    # em -> i
    for tag in soup.find_all("em"):
        tag.name = "i"

    # 3. Разворачиваем неподдерживаемые контейнеры (span, div, font, p),
    # сохраняя их внутренний текст и дочерние теги
    for tag in soup.find_all(
        ["span", "div", "font", "p", "section", "article"]
    ):
        tag.unwrap()

    # 4. Удаляем все атрибуты у тегов (style, class, id и т.д.),
    # кроме href у ссылок <a>
    for tag in soup.find_all(True):
        if tag.name == "a":
            href = tag.get("href")
            tag.attrs = {"href": href} if href else {}
        elif tag.name in ["b", "strong", "i", "em", "u", "s", "code", "pre"]:
            tag.attrs = {}
        else:
            # Если остался любой другой тег — просто убираем его оболочку
            tag.unwrap()

    # Получаем очищенную HTML-строку
    cleaned_html = str(soup)

    # 5. Убираем неразрывные пробелы (\xa0 / &nbsp;)
    cleaned_html = cleaned_html.replace("\xa0", " ").replace("&nbsp;", " ")

    # 6. Схлопываем избыточные пустые строки (более 2 подряд)
    cleaned_html = re.sub(r"\n\s*\n\s*\n+", "\n\n", cleaned_html).strip()

    return cleaned_html