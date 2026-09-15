from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.database import create_user
from app.keyboards import location

router=Router()

@router.message(CommandStart())
async def start(message: Message):
    await create_user(message.from_user.id)
    await message.answer(
        "🌤 <b>Привет!</b>\n\nЯ покажу погоду и подскажу, что надеть.\n"
        "Отправь местоположение или введи город вручную.",
        parse_mode="HTML", reply_markup=location()
    )
