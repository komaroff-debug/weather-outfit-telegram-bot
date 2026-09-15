from app.weather import description, wind_direction

def current(city, data):
    c, d = data["current"], data["daily"]
    return (
        f"📍 <b>{city}</b>\n\n"
        f"🌤 <b>{description(c['weather_code'])}</b>\n"
        f"🌡 Сейчас: <b>{c['temperature_2m']:+.1f}°C</b>\n"
        f"🤔 Ощущается: <b>{c['apparent_temperature']:+.1f}°C</b>\n"
        f"📊 Сегодня: <b>{d['temperature_2m_min'][0]:+.1f}...{d['temperature_2m_max'][0]:+.1f}°C</b>\n"
        f"💧 Влажность: <b>{c['relative_humidity_2m']}%</b>\n"
        f"💨 Ветер: <b>{c['wind_speed_10m']:.1f} м/с ({wind_direction(c['wind_direction_10m'])})</b>\n"
        f"🌬 Давление: <b>{c['pressure_msl']:.0f} гПа</b>\n"
        f"🌧 Вероятность осадков: <b>{d['precipitation_probability_max'][0]}%</b>\n"
        f"☔ Осадки: <b>{d['precipitation_sum'][0]:.1f} мм</b>"
    )

def hourly(city, data):
    h = data["hourly"]
    lines = [f"📍 <b>{city}</b>","", "🕐 <b>Почасовой прогноз</b>",""]
    for i,t in enumerate(h["time"]):
        lines.append(
            f"<b>{t[11:16]}</b> {h['temperature_2m'][i]:+.0f}°C "
            f"(ощущ. {h['apparent_temperature'][i]:+.0f}°C) | "
            f"🌧 {h['precipitation_probability'][i]}% | "
            f"💨 {h['wind_speed_10m'][i]:.0f} м/с"
        )
    return "\n".join(lines)

def outfit(city, a):
    text = f"📍 <b>{city}</b>\n\n👕 <b>Что надеть</b>\n\n🧥 <b>Одежда:</b>\n"
    text += "".join(f"• {x}\n" for x in a["clothes"])
    text += "\n👟 <b>Обувь:</b>\n" + "".join(f"• {x}\n" for x in a["shoes"])
    if a["accessories"]:
        text += "\n🎒 <b>Дополнительно:</b>\n" + "".join(f"• {x}\n" for x in a["accessories"])
    text += f"\n📊 <b>Комфорт на улице:</b> {a['score']}/10\n"
    if a["reasons"]:
        text += "\n💡 <b>Почему:</b>\n" + "".join(f"• {x}\n" for x in a["reasons"])
    return text
