from unittest.mock import patch

from app.telegram import create_bot


def test_create_bot_without_proxy():
    with patch("app.telegram.BOT_TOKEN", "123456:TEST_TOKEN"), patch(
        "app.telegram.TELEGRAM_PROXY", None
    ):
        bot = create_bot()
        try:
            assert bot.token == "123456:TEST_TOKEN"
        finally:
            import asyncio
            asyncio.run(bot.session.close())
