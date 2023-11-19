from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import ADMIN
from db import Database
from state.energy import Energy
from db_users import DatabaseUsers

router = Router()
db = Database()
db_users = DatabaseUsers()

@router.message(Command("add"))
async def add(message: Message, state: FSMContext):
    if message.from_user.username == ADMIN:
        await message.answer("Введите название напитка")
        await state.set_state(Energy.GET_TITLE)
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(Command("check"))
async def check(message: Message):
    if message.from_user.username == ADMIN:
        goods = await db.get()
        text = ""
        for item in goods:
            text = text + f"{item[0]} | {item[1]} {item[4]} | {item[3]} руб/шт | В наличии: {item[2]} шт. \n"
        await message.answer("Вот что у нас есть в наличии:\n\n" + text)
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(Command("change"))
async def change(message: Message, state: FSMContext):
    if message.from_user.username == ADMIN:
        await message.answer("Введите Id напитка, который хотите изменить")
        await state.set_state(Energy.GET_ID)
    else:
        await message.answer("У вас нет доступа к этой команде")


@router.message(Energy.GET_TITLE)
async def get_title(message: Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)
    await message.answer("Введите описание напитка")
    await state.set_state(Energy.GET_DESCRIPTION)


@router.message(Energy.GET_DESCRIPTION)
async def get_description(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await message.answer("Введите количество напитка")
    await state.set_state(Energy.GET_COUNT)


@router.message(Energy.GET_COUNT)
async def get_count(message: Message, state: FSMContext):
    count = message.text
    await state.update_data(count=count)
    await message.answer("Введите цену напитка")
    await state.set_state(Energy.GET_PRICE)


@router.message(Energy.GET_PRICE)
async def get_price(message: Message, state: FSMContext):
    price = message.text
    await state.update_data(price=price)
    data = await state.get_data()
    title = data.get("title")
    description = data.get("description")
    count = data.get("count")
    price = data.get("price")
    await db.add(title=title, count=count, price=price, description=description)
    await message.answer("Напиток добавлен")
    await state.clear()


@router.message(Energy.GET_ID)
async def get_id(message: Message, state: FSMContext):
    id = message.text
    await state.update_data(id=id)
    await message.answer("Введите количество напитка")
    await state.set_state(Energy.CHANGE_COUNT)


@router.message(Energy.CHANGE_COUNT)
async def change_count(message: Message, state: FSMContext):
    count = int(message.text)
    await state.update_data(count=count)
    data = await state.get_data()
    id = data.get("id")
    count = data.get("count")
    await db.change_count(id, count)
    await message.answer("Количество напитка изменено")
    await state.clear()


@router.message(Command("getusers"))
async def get_users(message: Message):
    if message.from_user.username == ADMIN:
        users = await db_users.get()
        text = ""
        for item in users:
            text = text + f"{item[0]} | {item[1]} \n"
        await message.answer("Вот все пользователи:\n\n" + text)
    else:
        await message.answer("У вас нет доступа к этой команде")
