import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handler import start as st
from handler.user import user_commands
from handler.admin import admin_commands
from handler import empty


from config import BOT_TOKEN
from db import Database
from db_users import DatabaseUsers


async def start() -> None:
    dp = Dispatcher()
    db = Database()
    db_users = DatabaseUsers()
    await db_users.create_table()
    await db.create_table()
    logging.basicConfig(level=logging.INFO)
    dp.include_router(st.router)
    dp.include_router(user_commands.router)
    dp.include_router(admin_commands.router)
    dp.include_router(empty.router)
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
