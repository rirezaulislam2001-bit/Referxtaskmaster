import aiosqlite

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
            screenshot TEXT,
            status TEXT DEFAULT 'pending'
        )
        """)

        await db.execute("""
        CREATE TABLE IF NOT EXISTS withdraws(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount INTEGER,
            method TEXT,
            number TEXT,
            status TEXT DEFAULT 'pending'
        )
        """)

        await db.commit()


async def add_user(user_id: int, referrer=None):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO users(user_id, referrer)
            VALUES (?, ?)
            """,
            (user_id, referrer)
        )
        await db.commit()


async def add_balance(user_id: int, amount: int):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (amount, user_id)
        )
        await db.commit()


async def get_balance(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT balance FROM users WHERE user_id = ?",
            (user_id,)
        )
        row = await cursor.fetchone()

        if row:
            return row[0]

        return 0


# ------------------ Deposit ------------------

async def save_deposit(user_id, amount, trxid, screenshot):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO deposits(user_id, amount, trxid, screenshot)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, amount, trxid, screenshot)
        )
        await db.commit()


async def get_pending_deposits():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT id, user_id, amount, trxid, screenshot
            FROM deposits
            WHERE status='pending'
        """)
        return await cursor.fetchall()


async def get_deposit(deposit_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            """
            SELECT user_id, amount, status
            FROM deposits
            WHERE id=?
            """,
            (deposit_id,)
        )
        return await cursor.fetchone()


async def approve_deposit(deposit_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE deposits SET status='approved' WHERE id=?",
            (deposit_id,)
        )
        await db.commit()


async def reject_deposit(deposit_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE deposits SET status='rejected' WHERE id=?",
            (deposit_id,)
        )
        await db.commit()


# ------------------ Withdraw ------------------

async def save_withdraw(user_id, amount, method, number):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """
            INSERT INTO withdraws(user_id, amount, method, number)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, amount, method, number)
        )
        await db.commit()


async def get_pending_withdraws():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("""
            SELECT id, user_id, amount, method, number
            FROM withdraws
            WHERE status='pending'
        """)
        return await cursor.fetchall()


async def approve_withdraw(withdraw_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE withdraws SET status='approved' WHERE id=?",
            (withdraw_id,)
        )
        await db.commit()


async def reject_withdraw(withdraw_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE withdraws SET status='rejected' WHERE id=?",
            (withdraw_id,)
        )
        await db.commit()
