from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import Database


async def choose_good() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    db = Database()
    goods = await db.get()
    for item in goods:
        if item[2] > 0:
            builder.row(types.InlineKeyboardButton(text=item[1], callback_data=str(item[0])))
    return builder.as_markup()
