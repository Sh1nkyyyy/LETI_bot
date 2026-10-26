import aiohttp
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from aiogram.types import BufferedInputFile

URL = "https://lk.etu.ru/api/user-announcement?current_page=1&page_size=5&total_entries=0"
DOWNLOAD_URL = "https://lk.etu.ru/dashboard/api/download/"
    
cookies = {
    "XSRF-TOKEN": "eyJpdiI6ImRCeEVVa0tYL24vRlZza3F3OTk3SkE9PSIsInZhbHVlIjoiREx2Qms0d1FmanVkZ0FodTlLOGVyUXpKWC9CcnNHdkNpYlBpcXdkemc3RzE1V1RzUVhZVGJXV2t2TVNkK3hLM1NGSE00ZDYxN2sxcVBBYUxoNkR4emc3ZXk2VG5tMUF4a3lWTmdGT0xWTWVKYkd4K05HRW4wSWpvL3ZPR2UzOVUiLCJtYWMiOiJhZWYwNjgxNjI2ODc2NWE5OWI2M2YyNjlhOWU1YTFjMWZhNTY0NzFlZTIwYzg3MDBlYmFkZjNjOGQ4ODE4MGJmIiwidGFnIjoiIn0%3D",
    "lk_etu_ru_session": "eyJpdiI6IjdpaGVuOCswa0wxYWYrY01hZ2dZbnc9PSIsInZhbHVlIjoiVElyenZocHdOVVAzRnUwUGk0RVBnTkxWNFQ1V1htMjVKV204SE9zK2FnTnZaZUh3OUdIOHVaNllHQmFvQWNoMUdvL2lnK0RkMW95VnFqcmZNdlhIVFEvWlYrckZxY2xib1gwRlRZeVJnVFZBNW1oSDdXRmJUdGY3bDRhZWxHTFgiLCJtYWMiOiIwOTkyNTVhNTk3MTExNmI5YTg0Y2UyMzJlNDQ3NTEzYjBiMWQyM2Y1MWRkMmVjZWI4NTQ3ZGEyNjE3Y2M5ZmVmIiwidGFnIjoiIn0%3D"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "X-Requested-With": "XMLHttpRequest",
}

async def fetch_announcements():
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        
        resp = await donwload_announcements(session)
        
        announcements = resp[1]
        
        if announcements:
            cleaned_announcements = []
            
            for announcement in announcements:
                
                announcement_dt = datetime.fromisoformat(announcement["date"]).replace(
                    tzinfo=ZoneInfo("Europe/Moscow")
                )
                
                if announcement_dt > (datetime.now(ZoneInfo("Europe/Moscow"))) - timedelta(hours=1):
                    
                    documents = []
                    docs_urls = []
                    
                    if announcement['files'] != []:
                        for file in announcement['files']:
                            file_name = file.get("name", "document")
                            file_ext = file.get("ext", "")
                            
                            full_filename = (
                                f"{file_name}.{file_ext}"
                                if file_ext and not file_name.endswith(f".{file_ext}")
                                else file_name
                            )     
                                          
                            url = DOWNLOAD_URL + str(file['id'])
                            docs_urls.append(url)
                            
                            file_bytes = await download_file_bytes(session, url)
                            
                            if not file_bytes:
                                continue
                            
                            document = BufferedInputFile(file=file_bytes, filename=full_filename)
                            documents.append(document)
                        
                    cleaned_announcement = {
                        "author": announcement["user"]["fio"],
                        "date": announcement["date"],
                        "text": announcement["content"].replace("<p>", "").replace("</p>", "").replace("<br>", "\n").strip(),
                        "theme": announcement['subject'],
                        "files": documents,
                        "files_urls": docs_urls
                    }
                    
                    cleaned_announcements.append(cleaned_announcement)
            
            return cleaned_announcements
            
            
async def donwload_announcements(session: aiohttp.ClientSession):
    async with session.get(URL) as response:
        print(f"Статус ответа: {response.status}")

        if response.status == 200:
            data = await response.json(encoding="utf-8")
            
            return data


async def download_file_bytes(
    session: aiohttp.ClientSession, url: str
) -> bytes | None:
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.read()
            else:
                print(
                    f"Ошибка скачивания файла (HTTP {response.status}): {url}"
                )
                return None
    except Exception as e:
        print(f"Исключение при скачивании файла {url}: {e}")
        return None


if __name__ == "__main__":
    asyncio.run(fetch_announcements())