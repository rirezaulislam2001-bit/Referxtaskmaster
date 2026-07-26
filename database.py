import aiosqlite
from config import ADMIN_ID
from aiogram import Bot
DB_NAME = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            balance INTEGER DEFAULT 0,
            referrer INTEGER
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS deposits(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount INTEGER,
            trxid TEXT,
            status TEXT DEFAULT 'pending'
        )
        """)

        await db.commit()
