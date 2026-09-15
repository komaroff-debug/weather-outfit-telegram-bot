import re
from aiogram import Router,F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.database import get_user,set_notification,set_notification_time
from app.keyboards import settings,main
from app.states import UserStates

router=Router()
TIME_RE=re.compile(r"^(?:[01]\d|2[0-3]):[0-5]\d$")

@router.message(F.text=="⚙️ Настройки")
async def settings_menu(message):
    u=await get_user(message.from_user.id)
    await message.answer(
        "⚙️ <b>Настройки</b>\n\n"
        f"🔔 Уведомления: {'включены' if u and u['notification_enabled'] else 'выключены'}\n"
        f"⏰ Время: {u['notification_time'] if u else '07:30'}",
        parse_mode="HTML",reply_markup=settings())

@router.message(F.text=="🔔 Включить уведомления")
async def enable(message):
    await set_notification(message.from_user.id,True)
    await message.answer("🔔 Уведомления включены.",reply_markup=settings())

@router.message(F.text=="🔕 Выключить уведомления")
async def disable(message):
    await set_notification(message.from_user.id,False)
    await message.answer("🔕 Уведомления выключены.",reply_markup=settings())

@router.message(F.text=="⏰ Изменить время уведомления")
async def ask_time(message,state):
    await state.set_state(UserStates.waiting_for_notification_time)
    await message.answer("⏰ Введи время HH:MM, например 07:30.")

@router.message(UserStates.waiting_for_notification_time)
async def save_time(message,state):
    value=message.text.strip()
    if not TIME_RE.fullmatch(value):
        await message.answer("❌ Неверный формат. Используй HH:MM.")
        return
    await set_notification_time(message.from_user.id,value)
    await state.clear()
    await message.answer(f"⏰ Установлено: <b>{value}</b>",parse_mode="HTML",reply_markup=settings())

@router.message(F.text=="🔙 Главное меню")
async def home(message,state):
    await state.clear()
    await message.answer("🏠 Главное меню",reply_markup=main())
