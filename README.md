# Weather Outfit Bot v1.2

Telegram-бот на Python + aiogram 3, который показывает погоду и рекомендует одежду и обувь.

## Возможности
- геолокация Telegram: кнопка «Отправить местоположение»;
- ручной выбор города;
- текущая погода;
- температура и ощущаемая температура;
- влажность, давление, ветер и направление ветра;
- вероятность и количество осадков;
- снег/дождь;
- прогноз на день;
- почасовой прогноз;
- рекомендация одежды, обуви и аксессуаров;
- режимы: общий, прогулка, работа, спорт;
- оценка комфорта 1–10;
- SQLite для хранения пользователя и настроек;
- утренние уведомления;
- часовой пояс определяется по координатам через Open-Meteo;
- FSM;
- logging;
- Docker;
- pytest;
- GitHub Actions;
- **опциональный HTTP/SOCKS-прокси только для Telegram Bot API**.

## Важно: если `api.telegram.org:443` недоступен

Если при запуске появляется:

```text
aiohttp.client_exceptions.ClientConnectorError:
Cannot connect to host api.telegram.org:443
```

проект можно запускать через прокси. В этом случае прокси используется только для Telegram, а Open-Meteo и Nominatim продолжают работать напрямую.

aiogram поддерживает HTTP tunneling и SOCKS4/4a/5 через `AiohttpSession`; для proxy connector нужен пакет `aiohttp-socks`.

### Настройка

1. Скопируйте `.env.example` в `.env`.
2. Укажите `BOT_TOKEN`.
3. Если Telegram API недоступен напрямую, укажите прокси, например:

```env
TELEGRAM_PROXY=http://127.0.0.1:8080
```

или:

```env
TELEGRAM_PROXY=socks5://127.0.0.1:1080
```

Для прокси с авторизацией:

```env
TELEGRAM_PROXY=socks5://LOGIN:PASSWORD@HOST:PORT
```

**Не публикуйте `.env` и не отправляйте его в GitHub.**

### Проверка Telegram-соединения

После активации виртуального окружения и установки зависимостей выполните:

```bash
python scripts/check_telegram.py
```

При успехе увидите примерно:

```text
Telegram proxy: socks5://127.0.0.1:1080
OK: @your_bot (id=123456789)
```

Если прокси не задан, скрипт проверит прямое подключение.

## Установка

1. Создайте бота через @BotFather.
2. Скопируйте `.env.example` в `.env`.
3. Укажите `BOT_TOKEN`.
4. Используйте Python 3.12.
5. Создайте окружение и активируйте его:

```bash
py -3.12 -m venv myvenv
myvenv\\Scripts\\activate
```

6. Установите зависимости:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Проверьте Telegram API:

```bash
python scripts/check_telegram.py
```

8. Запустите бота:

```bash
python bot.py
```

## Тесты

```bash
python -m pytest -q
```

## Docker

```bash
docker compose up -d --build
```

Параметр `TELEGRAM_PROXY` автоматически передаётся контейнеру через `.env`.

## Источники данных

Open-Meteo Forecast API, Open-Meteo Geocoding API и OpenStreetMap Nominatim.

## Структура

```text
weather_outfit_bot_v1_1/
├── app/
│   ├── handlers/
│   ├── clothing.py
│   ├── database.py
│   ├── formatters.py
│   ├── geocoding.py
│   ├── keyboards.py
│   ├── scheduler.py
│   ├── states.py
│   ├── telegram.py
│   └── weather.py
├── scripts/
│   └── check_telegram.py
├── tests/
├── bot.py
├── config.py
├── requirements.txt
└── .env.example
```
