from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.user import main_buttons
from db import db_users

router = Router()


@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    users = db_users.Users()
    get_by_id = await users.get_by_id(message.from_user.id)
    if not get_by_id:
        await users.add(userid=message.from_user.id, name=message.from_user.username, count_orders=0, is_active=True)
    await message.answer("Привет, " + message.from_user.full_name + "👋\n\n"
                         "Я бот-магазин энергетических напитков. Я помогу тебе зарядить твою батарейку 🔋.\n\n"
                         "Нажмите на кнопку «Купить» или «Наличие товаров» чтобы перейти к ассортименту",
                         reply_markup=main_buttons.buy_and_check_goods())


