"""Check Telegram Bot API connectivity using the same proxy as the bot.

Run from the project root:
    python scripts/check_telegram.py
"""

import asyncio
import sys
from pathlib import Path

# Allow execution as `python scripts/check_telegram.py` from project root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.telegram import create_bot  # noqa: E402
from config import TELEGRAM_PROXY  # noqa: E402


async def main() -> int:
    print(f"Telegram proxy: {TELEGRAM_PROXY or 'не задан (прямое подключение)'}")
    bot = create_bot()
    try:
        me = await bot.get_me()
        print(f"OK: @{me.username} (id={me.id})")
        return 0
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}")
        return 1
    finally:
        await bot.session.close()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
