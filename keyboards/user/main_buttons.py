from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def buy_and_check_goods() -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="Купить💰"))
    builder.row(types.KeyboardButton(text="Наличие товаров📃"))
    builder.row(types.KeyboardButton(text="Написать в поддержку📩"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
