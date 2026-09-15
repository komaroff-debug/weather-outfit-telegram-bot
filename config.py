import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/weather_bot.db")
DEFAULT_NOTIFICATION_TIME = os.getenv("DEFAULT_NOTIFICATION_TIME", "07:30")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Optional proxy used ONLY for Telegram Bot API requests.
# Examples:
#   http://127.0.0.1:8080
#   socks5://127.0.0.1:1080
#   socks5://user:password@host:port
TELEGRAM_PROXY = os.getenv("TELEGRAM_PROXY", "").strip() or None

if TELEGRAM_PROXY:
    allowed = ("http://", "https://", "socks4://", "socks4a://", "socks5://")
    if not TELEGRAM_PROXY.lower().startswith(allowed):
        raise ValueError(
            "TELEGRAM_PROXY должен начинаться с http://, https://, "
            "socks4://, socks4a:// или socks5://"
        )

