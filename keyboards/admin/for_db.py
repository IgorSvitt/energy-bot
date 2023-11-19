from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def db_commands() -> types.ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="Добавить"))
    builder.row(types.KeyboardButton(text="Удалить"))
    builder.row(types.KeyboardButton(text="Изменить"))
    builder.row(types.KeyboardButton(text="Посмотреть"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
