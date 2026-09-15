import aiohttp

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
REVERSE_URL = "https://nominatim.openstreetmap.org/reverse"

async def search_city(name):
    params = {"name": name, "count": 5, "language": "ru", "format": "json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(GEOCODING_URL, params=params,
                               timeout=aiohttp.ClientTimeout(total=10)) as r:
            r.raise_for_status()
            data = await r.json()
            return data.get("results", [])

async def reverse_geocode(lat, lon):
    params = {"lat": lat, "lon": lon, "format": "json", "accept-language": "ru"}
    headers = {"User-Agent": "WeatherOutfitTelegramBot/1.1"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(REVERSE_URL, params=params,
                               timeout=aiohttp.ClientTimeout(total=10)) as r:
            if r.status != 200:
                return "Ваше местоположение"
            data = await r.json()
            a = data.get("address", {})
            return (a.get("city") or a.get("town") or a.get("village")
                    or a.get("municipality") or "Ваше местоположение")
