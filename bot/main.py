
import asyncio
import logging
import sys
from config_data.config import config
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers import start_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, F, Dispatcher
from services.notificator import notify
from aiogram.types import LinkPreviewOptions


async def run_parser_job():
    print("Выполняю проверку новых уведомлений...")
    


async def main():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    
    bot = Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML, link_preview=LinkPreviewOptions(is_disabled=True)),
    )
    
    dp = Dispatcher()
    
    dp.include_router(start_router.router)
    
    
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(notify, trigger="cron", minute=0, args=(bot,))
    scheduler.start()
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("бот остановлен")