from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Bot

from db import Database
from state.energy import BuyEnergy
from keyboards.user.for_buy import choose_good

router = Router()
db = Database()


@router.message(F.text == "Купить💰")
async def buy(message: Message) -> None:
    goods = await choose_good()
    if not goods.inline_keyboard:
        await message.answer("Товар закончился")
    else:
        await message.answer("Выберите товар:", reply_markup=await choose_good())


@router.message(F.text == "Наличие товаров📃")
async def check_goods(message: Message) -> None:
    goods = await db.get()
    text = ""
    for item in goods:
        if item[2] > 0:
            text = text + f"{item[1]} {item[4]} | {item[3]} руб/шт | В наличии: {item[2]} шт. \n"
    if text == "":
        await message.answer("Товар закончился")
    else:
        await message.answer("Вот что у нас есть в наличии:\n\n" + text)


@router.callback_query(F.data)
async def check_goods(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    good_by_id = await db.get_by_id(int(callback.data))
    await state.update_data(title=good_by_id[0][1])
    await state.update_data(id=good_by_id[0][0])
    await callback.message.answer(f"Отправьте количество товара")
    await state.set_state(BuyEnergy.GET_COUNT)
    await callback.message.edit_reply_markup()


@router.message(BuyEnergy.GET_COUNT)
async def get_count(message: Message, state: FSMContext, bot: Bot):
    try:
        count = int(message.text)
        await state.update_data(count=count)
        data = await state.get_data()
        id = data.get("id")
        get_count = await db.get_by_id(int(id))
        if int(get_count[0][2]) < count:
            await message.answer("Такого количества нет в наличии")
        else:
            await message.answer("Спасибо за заказ! В ближайшее время с вами свяжется продавец")
            data = await state.get_data()
            try:
                await bot.send_message(chat_id=432188597, text=f"Новый заказ:\n"
                                                               f"Товар: {data['title']}\n"
                                                               f"Количество: {data['count']}\n"
                                                               f"user_id: @{message.from_user.username}")
                await state.clear()
            except Exception as e:
                print(f"Error: {e}")

        await db.change_count(int(id), int(get_count[0][2]) - count)
    except ValueError:
        await message.answer("Введите число")
