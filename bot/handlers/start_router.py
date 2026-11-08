from html import escape

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from services.rating_loader import get_6346_rating

router = Router()

@router.message(CommandStart())
async def start_message(message: Message):
    await message.answer("приветик")


@router.message(Command("rating"))
async def rating_message(message: Message):
    try:
        ratings = await get_6346_rating()
    except FileNotFoundError:
        await message.answer("Рейтинг пока недоступен: PDF ещё не скачан. Попробуйте позже.")
        return

    ranking = "\n".join(
        f"{student['рейтинг в группе']}. {escape(str(student['фио']))} — "
        f"{student['балл']:g} балл. (общее место: {student['рейтинг в общем списке']})"
        for student in ratings["участники"]
    )
    text = (
        "<b>Рейтинг группы 6346</b>\n"
        f"<blockquote expandable>{ranking or 'Нет участников'}</blockquote>\n\n"
        f"Средний балл: <b>{ratings['средний балл']:.2f}</b>\n"
        f"Место группы по среднему баллу: <b>{ratings['место группы']}</b>"
    )
    await message.answer(text, parse_mode="HTML")
