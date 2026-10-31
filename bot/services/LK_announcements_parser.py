import aiohttp
import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from aiogram.types import BufferedInputFile

URL = "https://lk.etu.ru/api/user-announcement?current_page=1&page_size=5&total_entries=0"
DOWNLOAD_URL = "https://lk.etu.ru/dashboard/api/download/"
    
cookies = {
    "XSRF-TOKEN": "eyJpdiI6IjZxMjhKb0dUR1JLcTBSTzVWQ2NHSkE9PSIsInZhbHVlIjoid08xMVZoL1g1Y3BWSnpQdURSKzhuT1JHeFd4K1ZGdFRlb1VicUZVYmtmUlNWTExzNXNZU2xNU1FKRE9CdHZrUUhoSG13ZDBwZ0hOYTNrY3dTQnc4YTE0Yk9xK2ltRk0vdWZ3SkpTTG9BY0RvMlB0bWt1bjZSNUF2K2duSCtWVUgiLCJtYWMiOiIwODZlYTIxN2FkYmUyYzg4MTIwMmM0M2I4NjI2OWUwMmEzMTYyYjg3MmZmZDc3ZDA4YWQ2YTFmYWM3YzAzZmNhIiwidGFnIjoiIn0%3D",
    "lk_etu_ru_session": "eyJpdiI6InV1cXdBWm5xSTZybFlsclF2ZFpTQ0E9PSIsInZhbHVlIjoiY0plSTA5Q3EySnFTcVU3VDh3VGZXeFo5aSs1TVhOWlEyRnRUYWs4RGFpSmNkNHpIM3BGQ0NWazNEa0NKZm5iMG5DWVNpNExhUXRXVStPcXY2OWZ2S09aN29UZ2dIQ29nZk5aN0NQN2lqaW1KMnZrVUIrdkx3cStqWkFXd25BL0QiLCJtYWMiOiIwMDQ2NmU5MWNiNmZkMjI1NzlkYmQ3YmM5OTNkYWQwYzc4Mzg3ZjFkOTFiNTcxNWE2YjU3MGQ2ZGU5MDI5Yjk2IiwidGFnIjoiIn0%3D"
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