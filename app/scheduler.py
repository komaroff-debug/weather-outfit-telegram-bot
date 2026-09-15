import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.database import get_notification_users,mark_notification_sent
from app.weather import get_weather
from app.clothing import advice
from app.formatters import outfit

log=logging.getLogger(__name__)
scheduler=AsyncIOScheduler()

async def notifications(bot):
    users=await get_notification_users()
    for u in users:
        try:
            tz=u["timezone"] or "UTC"
            now=datetime.now(ZoneInfo(tz))
            today=now.strftime("%Y-%m-%d")
            if now.strftime("%H:%M") != u["notification_time"] or u["last_notification_date"]==today:
                continue
            data=await get_weather(u["latitude"],u["longitude"])
            c,d=data["current"],data["daily"]
            a=advice(c["temperature_2m"],c["apparent_temperature"],c["relative_humidity_2m"],
                     d["precipitation_probability_max"][0],c["wind_speed_10m"],c["snowfall"],c["rain"],u["mode"] or "general")
            await bot.send_message(u["user_id"],"☀️ <b>Доброе утро!</b>\n\n"+outfit(u["city_name"],a),parse_mode="HTML")
            await mark_notification_sent(u["user_id"],today)
        except Exception:
            log.exception("notification error for %s",u["user_id"])

def start_scheduler(bot):
    scheduler.add_job(notifications,"interval",minutes=1,args=[bot],id="weather",replace_existing=True,max_instances=1,coalesce=True)
    scheduler.start()
