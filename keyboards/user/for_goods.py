from aiogram import types
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def categories_check_buttons(categories) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in categories:
        builder.row(types.InlineKeyboardButton(text=item[1], callback_data=("category_check_" + str(item[0]))))
    return builder.as_markup()


def back_check_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="back_check"))
    return builder.as_markup()


def back_buy_button() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Отмена", callback_data="back_buy"))
    return builder.as_markup()


def categories_buy_buttons(categories) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in categories:
        builder.row(types.InlineKeyboardButton(text=item[1], callback_data=("category_buy_" + str(item[0]))))
    return builder.as_markup()


def goods_for_sells_buttons(goods) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for good in goods:
        if good[3] == 0:
            continue
        text = f"{good[1]} {good[5]}| {good[2]} руб/шт |В наличие {good[3]} шт."
        builder.row(types.InlineKeyboardButton(text=text, callback_data=("good_buy_" + str(good[0]))))

    builder.row(types.InlineKeyboardButton(text="Назад", callback_data="back_buy"))

    return builder.as_markup()


def count_good_buy_buttons(good_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="1", callback_data=f"count_good_buy_{good_id}_1"))
    builder.row(types.InlineKeyboardButton(text="2", callback_data=f"count_good_buy_{good_id}_2"))
    builder.row(types.InlineKeyboardButton(text="3", callback_data=f"count_good_buy_{good_id}_3"))
    builder.row(types.InlineKeyboardButton(text="Отмена", callback_data="back_buy"))
    builder.adjust(3)
    return builder.as_markup()


def except_or_cancel_buttons() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Подтвердить", callback_data="except"))
    builder.row(types.InlineKeyboardButton(text="Отмена", callback_data="back_buy"))
    return builder.as_markup()





