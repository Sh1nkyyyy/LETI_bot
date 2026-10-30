from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

router = Router()

@router.message(CommandStart())
async def start_message(message: Message):
    await message.answer("приветик")
    