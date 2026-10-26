import html
import re
from bs4 import BeautifulSoup


def clean_lk_html_for_telegram(raw_html: str) -> str:
    if not raw_html:
        return ""

    soup = BeautifulSoup(raw_html, "html.parser")

    for img in soup.find_all("img"):
        alt_text = img.get("alt", "")
        img.replace_with(alt_text)

    for tag in soup.find_all("strong"):
        tag.name = "b"

    for tag in soup.find_all("em"):
        tag.name = "i"

    for tag in soup.find_all(
        ["span", "div", "font", "p", "section", "article"]
    ):
        tag.unwrap()

    for tag in soup.find_all(True):
        if tag.name == "a":
            href = tag.get("href")
            tag.attrs = {"href": href} if href else {}
        elif tag.name in ["b", "strong", "i", "em", "u", "s", "code", "pre"]:
            tag.attrs = {}
        else:
            tag.unwrap()

    cleaned_html = str(soup)

    cleaned_html = cleaned_html.replace("\xa0", " ").replace("&nbsp;", " ")

    cleaned_html = re.sub(r"\n\s*\n\s*\n+", "\n\n", cleaned_html).strip()

    return cleaned_html