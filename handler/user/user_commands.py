from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handler.user import good_methods
from keyboards.user import for_goods
from handler.user import user_methods
from state.energy import BuyGood

router = Router()


@router.message(F.text == "Наличие товаров📃")
async def check_goods(message: Message) -> None:
    categories = await good_methods.get_category()
    await message.answer("Выберите категорию:", reply_markup=for_goods.categories_check_buttons(categories))


@router.callback_query(F.data.startswith("category_check_"))
async def check_goods(callback: CallbackQuery) -> None:
    text, album = await good_methods.get_goods(int(callback.data.split("_")[2]))
    await callback.message.delete()
    if album is None:
        await callback.message.answer(text, reply_markup=for_goods.back_check_button())
        return

    album.caption = text
    await callback.message.answer_media_group(album.build())


@router.callback_query(F.data == "back_check")
async def check_goods(callback: CallbackQuery) -> None:
    categories = await good_methods.get_category()
    await callback.message.delete()
    await callback.message.answer("Выберите категорию:", reply_markup=for_goods.categories_check_buttons(categories))


@router.message(F.text == "Купить💰")
async def buy(message: Message) -> None:
    categories = await good_methods.get_category()
    await message.answer("Выберите категорию:", reply_markup=for_goods.categories_buy_buttons(categories))


@router.callback_query(F.data.startswith("category_buy_"))
async def buy(callback: CallbackQuery) -> None:
    goods = await good_methods.get_goods_for_sell(int(callback.data.split("_")[2]))
    await callback.message.delete()
    if not goods:
        await callback.message.answer("Товар закончился", reply_markup=for_goods.back_buy_button())
        return

    await callback.message.answer("Выберите товар:", reply_markup=for_goods.goods_for_sells_buttons(goods))


@router.callback_query(F.data == "back_buy")
async def buy(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    categories = await good_methods.get_category()
    await callback.message.delete()
    await callback.message.answer("Выберите категорию:", reply_markup=for_goods.categories_buy_buttons(categories))


@router.callback_query(F.data.startswith("good_buy_"))
async def good_for_sell(callback: CallbackQuery, state: FSMContext) -> None:
    text = await good_methods.get_good_for_sell(callback.data.split("_")[2])
    await callback.message.delete()
    await callback.message.answer(text=text, reply_markup=for_goods.count_good_buy_buttons(callback.data.split("_")[2]))
    await state.update_data(id=callback.data.split("_")[2])
    await state.set_state(BuyGood.GET_COUNT)
    await state.update_data(id=callback.data.split("_")[2])


@router.callback_query(F.data.startswith("count_good_buy_"))
async def get_good_count_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_reply_markup()
    count = await good_methods.get_good_count(callback.data.split("_")[3])
    if count < int(callback.data.split("_")[4]):
        await callback.message.answer("Такого количества нет в наличии")
        return
    await callback.message.answer("Укажите куда доставить товар")
    await state.update_data(count=int(callback.data.split("_")[4]))
    await state.set_state(BuyGood.GET_ROOM)


@router.message(BuyGood.GET_COUNT)
async def get_good_count_message(message: Message, state: FSMContext) -> None:
    try:
        data = await state.get_data()
        id = data.get("id")
        count = await good_methods.get_good_count(id)
        if count < int(message.text):
            await message.answer("Такого количества нет в наличии")
            return
        await message.answer("Укажите куда доставить товар")
        await state.update_data(count=int(message.text))
        await state.set_state(BuyGood.GET_ROOM)
    except ValueError:
        await message.answer("Неверное значение")


@router.message(BuyGood.GET_ROOM)
async def buy_good(message: Message, state: FSMContext) -> None:
    await state.update_data(room=message.text)
    data = await state.get_data()
    id = data.get("id")
    count = data.get("count")
    room = data.get("room")
    text = await good_methods.check_info(id, count, room)
    await message.answer(text, reply_markup=for_goods.except_or_cancel_buttons())


@router.callback_query(F.data == "except")
async def except_good(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await callback.message.edit_reply_markup()
    data = await state.get_data()
    id = data.get("id")
    count = data.get("count")
    room = data.get("room")
    user_id = callback.from_user.id
    username = callback.from_user.username
    await user_methods.send_order_to_admins(user_id=user_id, good_id=id, count=count, room=room, user_name=username, bot=bot)
    await state.clear()
    await good_methods.write_order(user_id=callback.from_user.id, good_id=id, count=count)
    text = "Спасибо за покупку!\n" \
           "Ваш заказ принят в обработку.\n" \
           "Скоро с вами свяжется наш менеджер. \n\n" \
           "P.S Если вам понравился наш сервис, то, пожалуйста, оставьте отзыв в беседе <a href='https://vk.me/join/sTUXxbQAt1KI_CO7dTq1ypYgYyv1Ica1b10='>лакокрасочных🥺</a>"
    await callback.message.answer(text)


@router.message(F.text == "Написать в поддержку📩")
async def write_to_support(message: Message) -> None:
    await message.answer("Напишите в лс @nik0laevig0r или @alomatov")









