import aiosqlite
DB_PATH = "bot.db"
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        await db.execute("CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, service_id INTEGER, date TEXT)")
        await db.commit()
async def get_or_create_user(user_id, name):
    async with aiosqlite.connect(DB_PATH) as db:
        if not await (await db.execute("SELECT id FROM users WHERE id=?", (user_id,))).fetchone():
            await db.execute("INSERT INTO users VALUES (?,?)", (user_id, name))
            await db.commit()
async def create_appointment(user_id, service_id, date):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO appointments (user_id, service_id, date) VALUES (?,?,?)", (user_id, service_id, date))
        await db.commit()
