from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

router = Router()

@router.message(CommandStart())
async def start_message(message: Message):
    await message.answer("приветик")
    
@router.message()
async def get_topic_info(message: Message):
    print("----- ДАННЫЕ О ЧАТЕ И ВЕТКЕ -----")
    print(f"Chat ID (ID группы): {message.chat.id}")
    print(f"Chat Title: {message.chat.title}")
    print(f"Thread ID (ID ветки): {message.message_thread_id}")
    print("---------------------------------")

    # Можно ответить прямо в чат:
    