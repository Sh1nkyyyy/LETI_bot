import io
import aiohttp

prog_url = "https://disk.yandex.ru/d/-BY6WYZSSFa40A"

async def fetch_pdf_bytes(
    session: aiohttp.ClientSession
) -> io.BytesIO:
    async with session.get(prog_url) as resp:
        resp.raise_for_status()
        content = await resp.read()
        return io.BytesIO(content)
    
    
async def parse_rating():
    ...