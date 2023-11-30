from aiogram.dispatcher.event.bases import CancelHandler

from aiogram import types, BaseMiddleware
from config import ADMIN_IDS

class BotStatusMiddleware(BaseMiddleware):
    def __init__(self):
        super(BotStatusMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        with open('bot_status.txt', 'r') as file:
            status = file.read().strip()
            if status.lower() != 'on' and message.from_user.id not in ADMIN_IDS:
                await message.answer('Бот в данный момент неактивен.')
                raise CancelHandler()



