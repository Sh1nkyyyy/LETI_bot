import aiohttp
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from aiogram.types import BufferedInputFile
from services.cleaner_html import clean_lk_html_for_telegram

from config_data.config import config

URL = "https://lk.etu.ru/api/user-announcement?current_page=1&page_size=5&total_entries=0"
DOWNLOAD_URL = "https://lk.etu.ru/dashboard/api/download/"
    
cookies = {
    "XSRF-TOKEN": config.lk_xsrf_token.get_secret_value(),
    "lk_etu_ru_session": config.lk_cookie_session.get_secret_value() 
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
                
                if announcement_dt > (datetime.now(ZoneInfo("Europe/Moscow"))) - timedelta(seconds=config.parser_check_interval):
                    
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
                        "text": clean_lk_html_for_telegram(announcement["content"]),
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
