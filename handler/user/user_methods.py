from aiogram import Bot
from db import db_goods

from config import ADMIN_IDS

db_goods = db_goods.Goods()


async def send_order_to_admins(good_id, count, room, user_name, user_id, bot: Bot):
    admins = ADMIN_IDS
    good = await db_goods.get_by_id(good_id)
    title = good[1]
    for admin in admins:
        await bot.send_message(admin, f"Новый заказ:\n"
                                      f"Товар: {title}\n"
                                      f"Количество: {count}\n"
                                      f"Комната: {room}\n"
                                      f"user: @{user_name}")
