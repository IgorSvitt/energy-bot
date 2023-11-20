from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Bot
import logging

from aiogram.utils.media_group import MediaGroupBuilder

from db import Database
from db_users import DatabaseUsers
from state.energy import BuyEnergy
from keyboards.user.for_buy import choose_good, cancel

router = Router()
db = Database()
db_users = DatabaseUsers()


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
    media = MediaGroupBuilder()
    for item in goods:
        if item[2] > 0:
            media.add(
                type="photo",
                media=FSInputFile("photos/"+item[5]+".jpg"),
            )
            text = text + f"<b>{item[1]}</b> {item[4]} | {item[3]} руб/шт | В наличии: {item[2]} шт. \n\n"
    if text == "":
        await message.answer("Товар закончился")
    else:
        media.caption = text
        await message.answer_media_group(media.build())


@router.callback_query(F.data)
async def check_goods(callback: CallbackQuery, state: FSMContext) -> None:
    good_by_id = await db.get_by_id(int(callback.data))
    await state.update_data(title=good_by_id[0][1])
    await state.update_data(id=good_by_id[0][0])
    await callback.message.answer(f"Отправьте количество товара")
    await state.set_state(BuyEnergy.GET_COUNT)
    await callback.message.edit_reply_markup()


@router.message(BuyEnergy.GET_COUNT)
async def get_count(message: Message, state: FSMContext,):
    try:
        count = int(message.text)
        await state.update_data(count=count)
        data = await state.get_data()
        id = data.get("id")
        get_count = await db.get_by_id(int(id))
        if int(get_count[0][2]) < count:
            await message.answer("Такого количества нет в наличии")
        else:
            await message.answer("Введите номер комнаты")
            await state.set_state(BuyEnergy.GET_ROOM)

    except ValueError:
        await message.answer("Введите число")


@router.message(BuyEnergy.GET_ROOM)
async def get_room(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(room=message.text)
    await message.answer("Спасибо за заказ! В ближайшее время с вами свяжется продавец")
    data = await state.get_data()
    id = data.get("id")
    get_count = await db.get_by_id(int(id))
    try:
        await bot.send_message(chat_id=432188597, text=f"Новый заказ:\n"
                                                       f"Товар: {data['title']}\n"
                                                       f"Количество: {data['count']}\n"
                                                       f"Комната: {data['room']}\n"
                                                       f"user_id: @{message.from_user.username}")
        await bot.send_message(chat_id=403062158, text=f"Новый заказ:\n"
                                                       f"Товар: {data['title']}\n"
                                                       f"Количество: {data['count']}\n"
                                                       f"Комната: {data['room']}\n"
                                                       f"user_id: @{message.from_user.username}")
        await db.update_count(int(id), int(get_count[0][2]) - int(data['count']))
        await state.clear()
        count = await db_users.get_count(int(id))
        if count[0] is None:
            count = 0
        count = count[0] + 1
        await db_users.update_count(int(id), count)

    except Exception as e:
        logging.error(e)

