"""Telegram Bot API client factory.

The project normally connects directly to Telegram. If the current network
cannot reach api.telegram.org:443, set TELEGRAM_PROXY in .env. The proxy is
applied only to Telegram API traffic; weather/geocoding requests remain direct.
"""

from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession

from config import BOT_TOKEN, TELEGRAM_PROXY


def create_bot() -> Bot:
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден в .env")
    session = AiohttpSession(proxy=TELEGRAM_PROXY)
    return Bot(token=BOT_TOKEN, session=session)
