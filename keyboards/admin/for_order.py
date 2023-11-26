from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_mailing() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Отправить", callback_data="send_request"))
    builder.row(types.InlineKeyboardButton(text="Отмена", callback_data="cancel_request"))
    return builder.as_markup()