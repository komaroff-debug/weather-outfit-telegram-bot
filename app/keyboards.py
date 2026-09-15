from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🌤 Погода сейчас"),KeyboardButton(text="👕 Что надеть?")],
        [KeyboardButton(text="📅 Прогноз на сегодня"),KeyboardButton(text="🕐 По часам")],
        [KeyboardButton(text="📍 Изменить город"),KeyboardButton(text="🚶 Прогулка")],
        [KeyboardButton(text="💼 Работа"),KeyboardButton(text="🏃 Спорт")],
        [KeyboardButton(text="⚙️ Настройки")]
    ], resize_keyboard=True)

def location():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="📍 Отправить местоположение", request_location=True)],
        [KeyboardButton(text="🏙 Ввести город")]
    ], resize_keyboard=True)

def cities(results):
    rows=[]
    for x in results:
        label=x["name"]
        if x.get("admin1"): label += f", {x['admin1']}"
        if x.get("country"): label += f" ({x['country']})"
        rows.append([KeyboardButton(text=label)])
    rows.append([KeyboardButton(text="❌ Отмена")])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

def settings():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="🔔 Включить уведомления")],
        [KeyboardButton(text="🔕 Выключить уведомления")],
        [KeyboardButton(text="⏰ Изменить время уведомления")],
        [KeyboardButton(text="🔙 Главное меню")]
    ], resize_keyboard=True)
