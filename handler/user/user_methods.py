from aiogram import Bot
from db import db_goods

from config import ADMIN_IDS

from keyboards.admin import for_order

db_goods = db_goods.Goods()


async def send_order_to_admins(good_id, count, room, user_name, user_id, bot: Bot):
    admins = ADMIN_IDS
    good = await db_goods.get_by_id(good_id)
    title = good[1] + " " + good[5]
    for admin in admins:
        await bot.send_message(admin, f"Новый заказ:\n"
                                      f"Товар: {title}\n"
                                      f"Количество: {count}\n"
                                      f"Заказ на сумму: {good[2] * count}\n"
                                      f"Комната: {room}\n"
                                      f"user: @{user_name}")


async def send_feedback_to_admins(text, user_name, bot: Bot):
    admins = ADMIN_IDS
    text = f"Новый отзыв:\n" \
           f"{text}\n" \
           f"user: @{user_name}"
    for admin in admins:
        await bot.send_message(admin, text=text)


