import asyncio

from aiogram import Dispatcher

from app.database import init_db
from app.logging_config import setup_logging
from app.scheduler import start_scheduler
from app.telegram import create_bot
from app.handlers.start import router as start_router
from app.handlers.weather import router as weather_router
from app.handlers.settings import router as settings_router


async def main():
    setup_logging()
    await init_db()

    bot = create_bot()
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(weather_router)
    dp.include_router(settings_router)
    start_scheduler(bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
