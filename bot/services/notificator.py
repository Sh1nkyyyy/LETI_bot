from aiogram import Bot
import aiohttp
from services.LK_announcements_parser import fetch_announcements
from services.RC_parser import fetch_messages
from services.cleaner_html import clean_lk_html_for_telegram
from templates import formatting_RK_message, formatting_LK_announcements


rc_chat_id = "-1003337617897"
notifications_chat_id = "-1003337617897"

async def notify(bot: Bot):
    rocket_chat_messages = await fetch_messages()
    if rocket_chat_messages:
        for chat, messages in rocket_chat_messages.items():
            for msg in messages:
                try:
                    await bot.send_message(
                        chat_id=rc_chat_id,
                        **formatting_RK_message(chat, msg['author'], msg['text'], msg['date'])
                    )
                except Exception as e:
                    print(f"Не удалось отправить уведомление {rc_chat_id}: {e}")
                    
                    
    lk_notifications = await fetch_announcements()
    if lk_notifications:
        for msg in lk_notifications:
            text = clean_lk_html_for_telegram(msg["text"])
            try:
                await bot.send_message(
                    chat_id=notifications_chat_id,
                    **formatting_LK_announcements(msg["theme"], msg['author'], clean_lk_html_for_telegram(msg['text']), msg['date'])
                )
            except Exception as e:
                print(f"Не удалось отправить уведомление {rc_chat_id}: {e}", text)    
            for file in msg["files"]:
                try:
                    await bot.send_document(
                        chat_id=notifications_chat_id,
                        document=file,
                    )
                except Exception as e:
                    print(f"Не удалось отправить файл {rc_chat_id}: {e}")

        