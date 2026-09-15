import aiohttp

URL = "https://api.open-meteo.com/v1/forecast"

CODES = {
0:"Ясно",1:"Преимущественно ясно",2:"Переменная облачность",3:"Пасмурно",
45:"Туман",48:"Изморозь",51:"Морось",53:"Морось",55:"Сильная морось",
56:"Ледяная морось",57:"Сильная ледяная морось",61:"Небольшой дождь",
63:"Дождь",65:"Сильный дождь",66:"Ледяной дождь",67:"Сильный ледяной дождь",
71:"Небольшой снег",73:"Снег",75:"Сильный снег",77:"Снежные зёрна",
80:"Ливень",81:"Сильный ливень",82:"Очень сильный ливень",
85:"Снегопад",86:"Сильный снегопад",95:"Гроза",96:"Гроза с градом",
99:"Сильная гроза с градом"
}

async def get_weather(lat, lon):
    params = {
        "latitude": lat, "longitude": lon,
        "current": ",".join([
            "temperature_2m","relative_humidity_2m","apparent_temperature",
            "precipitation","rain","showers","snowfall","weather_code",
            "cloud_cover","pressure_msl","wind_speed_10m","wind_direction_10m"
        ]),
        "hourly": ",".join([
            "temperature_2m","apparent_temperature",
            "precipitation_probability","precipitation","rain","snowfall",
            "wind_speed_10m","relative_humidity_2m","weather_code"
        ]),
        "daily": ",".join([
            "weather_code","temperature_2m_max","temperature_2m_min",
            "apparent_temperature_max","apparent_temperature_min",
            "precipitation_probability_max","precipitation_sum","rain_sum",
            "snowfall_sum","wind_speed_10m_max","sunrise","sunset"
        ]),
        "timezone": "auto", "forecast_days": 1
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params=params,
                               timeout=aiohttp.ClientTimeout(total=10)) as r:
            r.raise_for_status()
            return await r.json()

def description(code):
    return CODES.get(code, "Неизвестные условия")

def wind_direction(degrees):
    dirs = ["С","СВ","В","ЮВ","Ю","ЮЗ","З","СЗ"]
    return dirs[round(degrees / 45) % 8]
