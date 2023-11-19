from aiogram import Router
from aiogram.types import Message

from keyboards.user import main_buttons

router = Router()


@router.message()
async def empty_command(message: Message) -> None:
    await message.answer(text="Нажмите на кнопку «Купить» или «Наличие товаров» чтобы перейти к ассортименту",
                         reply_markup=main_buttons.buy_and_check_goods())
