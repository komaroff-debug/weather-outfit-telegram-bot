from pathlib import Path
import aiosqlite
from config import DATABASE_PATH, DEFAULT_NOTIFICATION_TIME

async def init_db():
    Path(DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                city_name TEXT,
                latitude REAL,
                longitude REAL,
                timezone TEXT DEFAULT 'UTC',
                notification_enabled INTEGER DEFAULT 0,
                notification_time TEXT DEFAULT '07:30',
                mode TEXT DEFAULT 'general',
                last_notification_date TEXT
            )
        ''')
        await db.commit()

async def create_user(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, notification_time) VALUES (?, ?)",
            (user_id, DEFAULT_NOTIFICATION_TIME)
        )
        await db.commit()

async def save_location(user_id, city, lat, lon, timezone):
    await create_user(user_id)
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET city_name=?, latitude=?, longitude=?, timezone=? WHERE user_id=?",
            (city, lat, lon, timezone, user_id)
        )
        await db.commit()

async def get_user(user_id):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        return await cur.fetchone()

async def set_mode(user_id, mode):
    await create_user(user_id)
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("UPDATE users SET mode=? WHERE user_id=?", (mode, user_id))
        await db.commit()

async def set_notification(user_id, enabled):
    await create_user(user_id)
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET notification_enabled=? WHERE user_id=?",
            (int(enabled), user_id)
        )
        await db.commit()

async def set_notification_time(user_id, time):
    await create_user(user_id)
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET notification_time=? WHERE user_id=?",
            (time, user_id)
        )
        await db.commit()

async def get_notification_users():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM users WHERE notification_enabled=1 AND latitude IS NOT NULL"
        )
        return await cur.fetchall()

async def mark_notification_sent(user_id, date):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET last_notification_date=? WHERE user_id=?",
            (date, user_id)
        )
        await db.commit()
