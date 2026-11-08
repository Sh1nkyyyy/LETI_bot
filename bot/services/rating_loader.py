import asyncio
from pathlib import Path
import aiohttp
import pdfplumber
import pandas as pd

prog_url = "https://disk.yandex.ru/d/-BY6WYZSSFa40A"
api_url = "https://cloud-api.yandex.net/v1/disk/public/resources/download"
RATING_PDF_PATH = Path(__file__).resolve().parents[2] / "data" / "rating.pdf"

headers = {
    "фио": 0,
    "группа": 1,
    "логин": 2,
    "id": 3,
    "почта": 4,
    "github": 5,
    "лр1": 6,
    "лр2": 7,
    "лр3": 8,
    "лр4": 9,
    "курс": 10,
    "гит": 11,
    "линукс": 12,
    "штрафные": 13,
    "бонусные": 14,
    "контрольная": 15,
    "прокторинг_кр": 16,
    "балл": 17,
    "проблемы": 18,
    "оценка": 19,
    "дата_пр_курсовой": 20,
    "оценка_пр_курсовой": 21,
    "оценка_курсовой": 22,
    "период_сдачи": 23,
    "отчислен": 24
}


async def fetch_prog_file():
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, params={"public_key": prog_url}) as response:
            response.raise_for_status()
            data = await response.json()

        async with session.get(data["href"]) as response:
            response.raise_for_status()
            content = await response.read()

    RATING_PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    RATING_PDF_PATH.write_bytes(content)


async def get_6346_rating() -> dict:
    with pdfplumber.open(RATING_PDF_PATH) as pdf:
        table = []
        for page in pdf.pages:
            page_table = page.extract_table()
            if page_table:
                table.extend(page_table)


    del table[0:2]
    df = pd.DataFrame(table, columns=headers.keys())

    students = df[["фио", "группа", "балл"]].copy()
    students["группа"] = pd.to_numeric(students["группа"], errors="coerce")
    students["балл"] = pd.to_numeric(
        students["балл"].astype("string").str.strip().str.replace(",", ".", regex=False),
        errors="coerce",
    )
    students = students.loc[
        (students["группа"] <= 6346)
    ].copy()
    students["рейтинг в общем списке"] = (
        students["балл"].rank(ascending=False, method="min").astype("Int64")
    )

    group = students.loc[students["группа"] == 6346].copy()
    group["рейтинг в группе"] = (
        group["балл"].rank(ascending=False, method="min").astype("Int64")
    )
    group_averages = students.groupby("группа")["балл"].mean()
    group_ranks = group_averages.rank(ascending=False, method="min")

    participants = (
        group.sort_values(["рейтинг в группе", "фио"])[
            ["фио", "балл", "рейтинг в группе", "рейтинг в общем списке"]
        ]
        .to_dict(orient="records")
    )
    return {
        "участники": participants,
        "средний балл": float(group_averages.loc[6346]),
        "место группы": int(group_ranks.loc[6346]),
    }