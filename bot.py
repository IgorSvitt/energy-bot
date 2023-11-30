import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeDefault, BotCommandScopeChat

from handler import start as st
from handler.user import user_commands
from handler.admin import admin_commands
from handler import empty
from commands import cmd_admins

from middleware.change_status import BotStatusMiddleware


from config import BOT_TOKEN, ADMIN_IDS
from db import db_users, db_categories, db_goods, db_orders


async def start() -> None:

    users = db_users.Users()
    categories = db_categories.Categories()
    goods = db_goods.Goods()
    orders = db_orders.Orders()
    await users.create_table()
    await categories.create_table()
    await goods.create_table()
    await orders.create_table()

    # test
    # await categories.create_test_data()
    # await goods.create_test_data()

    dp = Dispatcher()
    dp.update.middleware(BotStatusMiddleware())
    logging.basicConfig(level=logging.INFO)
    dp.include_router(st.router)
    dp.include_router(admin_commands.router)
    dp.include_router(user_commands.router)
    dp.include_router(empty.router)
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    for admin in ADMIN_IDS:
        await bot.set_my_commands(commands=cmd_admins.admin_commands, scope=BotCommandScopeChat(chat_id=admin))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
