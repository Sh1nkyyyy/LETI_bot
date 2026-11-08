
import asyncio
import logging
import sys
from datetime import datetime
from config_data.config import config
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers import start_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from services.notificator import notify
from services.rating_loader import fetch_prog_file
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
    scheduler.add_job(notify, trigger="interval", seconds=config.parser_check_interval, args=(bot,))
    scheduler.add_job(
        fetch_prog_file, trigger="interval", hours=6,
        next_run_time=datetime.now(scheduler.timezone),
    )
    scheduler.start()

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown(wait=False)
        await bot.session.close()



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("бот остановлен")
