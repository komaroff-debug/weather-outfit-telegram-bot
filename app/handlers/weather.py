import logging
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.database import save_location,get_user,set_mode
from app.geocoding import reverse_geocode,search_city
from app.weather import get_weather
from app.clothing import advice
from app.formatters import current,hourly,outfit
from app.keyboards import main,location,cities
from app.states import UserStates

router=Router()
log=logging.getLogger(__name__)

async def no_location(message):
    await message.answer("Сначала укажи город.",reply_markup=location())

@router.message(F.location)
async def geo(message,state:FSMContext):
    try:
        lat,lon=message.location.latitude,message.location.longitude
        city=await reverse_geocode(lat,lon)
        data=await get_weather(lat,lon)
        await save_location(message.from_user.id,city,lat,lon,data.get("timezone","UTC"))
        await state.clear()
        await message.answer(current(city,data),parse_mode="HTML",reply_markup=main())
    except Exception:
        log.exception("location error")
        await message.answer("❌ Не удалось получить данные. Попробуй ещё раз.",reply_markup=location())

@router.message(F.text=="🏙 Ввести город")
async def ask_city(message,state:FSMContext):
    await state.set_state(UserStates.waiting_for_city)
    await message.answer("🏙 Напиши название города.")

@router.message(UserStates.waiting_for_city)
async def city_search(message,state:FSMContext):
    results=await search_city(message.text.strip())
    if not results:
        await message.answer("❌ Город не найден.")
        return
    await state.update_data(results=results)
    await state.set_state(UserStates.choosing_city)
    await message.answer("Выбери подходящий вариант:",reply_markup=cities(results))

@router.message(UserStates.choosing_city)
async def choose(message,state:FSMContext):
    if message.text=="❌ Отмена":
        await state.clear()
        await message.answer("Отменено.",reply_markup=main())
        return
    data=await state.get_data()
    selected=None
    for x in data.get("results",[]):
        label=x["name"]
        if x.get("admin1"): label+=f", {x['admin1']}"
        if x.get("country"): label+=f" ({x['country']})"
        if label==message.text:
            selected=x;break
    if not selected:
        await message.answer("Выбери город кнопкой.")
        return
    weather=await get_weather(selected["latitude"],selected["longitude"])
    await save_location(message.from_user.id,selected["name"],selected["latitude"],selected["longitude"],weather.get("timezone","UTC"))
    await state.clear()
    await message.answer(current(selected["name"],weather),parse_mode="HTML",reply_markup=main())

@router.message(F.text=="📍 Изменить город")
async def change(message,state):
    await state.clear()
    await message.answer("📍 Отправь геолокацию или выбери ввод города.",reply_markup=location())

@router.message(F.text=="🌤 Погода сейчас")
async def now(message):
    u=await get_user(message.from_user.id)
    if not u or u["latitude"] is None: return await no_location(message)
    await message.answer(current(u["city_name"],await get_weather(u["latitude"],u["longitude"])),parse_mode="HTML")

@router.message(F.text=="🕐 По часам")
async def hours(message):
    u=await get_user(message.from_user.id)
    if not u or u["latitude"] is None: return await no_location(message)
    await message.answer(hourly(u["city_name"],await get_weather(u["latitude"],u["longitude"])),parse_mode="HTML")

async def show_outfit(message,mode):
    u=await get_user(message.from_user.id)
    if not u or u["latitude"] is None: return await no_location(message)
    await set_mode(message.from_user.id,mode)
    data=await get_weather(u["latitude"],u["longitude"])
    c,d=data["current"],data["daily"]
    a=advice(c["temperature_2m"],c["apparent_temperature"],c["relative_humidity_2m"],
             d["precipitation_probability_max"][0],c["wind_speed_10m"],c["snowfall"],c["rain"],mode)
    await message.answer(outfit(u["city_name"],a),parse_mode="HTML")

@router.message(F.text=="👕 Что надеть?")
async def clothes(message): await show_outfit(message,"general")
@router.message(F.text=="🚶 Прогулка")
async def walk(message): await show_outfit(message,"walk")
@router.message(F.text=="💼 Работа")
async def work(message): await show_outfit(message,"work")
@router.message(F.text=="🏃 Спорт")
async def sport(message): await show_outfit(message,"sport")

@router.message(F.text=="📅 Прогноз на сегодня")
async def daily(message):
    u=await get_user(message.from_user.id)
    if not u or u["latitude"] is None: return await no_location(message)
    d=(await get_weather(u["latitude"],u["longitude"]))["daily"]
    text=(f"📅 <b>{u['city_name']} — сегодня</b>\n\n"
          f"🌡 {d['temperature_2m_min'][0]:+.1f}...{d['temperature_2m_max'][0]:+.1f}°C\n"
          f"🤔 Ощущается: {d['apparent_temperature_min'][0]:+.1f}...{d['apparent_temperature_max'][0]:+.1f}°C\n"
          f"🌧 Осадки: {d['precipitation_probability_max'][0]}%\n"
          f"☔ Количество: {d['precipitation_sum'][0]:.1f} мм\n"
          f"💨 Максимальный ветер: {d['wind_speed_10m_max'][0]:.1f} м/с\n"
          f"🌅 Восход: {d['sunrise'][0][11:16]}\n🌇 Закат: {d['sunset'][0][11:16]}")
    await message.answer(text,parse_mode="HTML")
