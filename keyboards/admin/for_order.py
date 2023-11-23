from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_accept_or_deny(user_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Принять", callback_data="accept_" + str(user_id)))
    builder.row(types.InlineKeyboardButton(text="Отклонить", callback_data="deny_" + str(user_id)))
    return builder.as_markup()
