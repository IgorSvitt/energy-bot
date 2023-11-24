from aiogram.types import BotCommand

admin_commands = [
    BotCommand(command="/start", description="Начать работу"),
    BotCommand(command="/add", description="Добавить товар"),
    BotCommand(command="/get", description="Посмотреть товары"),
    BotCommand(command="/delete", description="Удалить товар"),
    BotCommand(command="/cancel", description="Отменить действие"),
    BotCommand(command="/updatecount", description="Изменить количество товара"),
    BotCommand(command="/getusers", description="Посмотреть пользователей"),
    BotCommand(command="/addcategory", description="Добавить категорию"),
    BotCommand(command="/getcategories", description="Посмотреть категории"),
    BotCommand(command="/deletecategory", description="Удалить категорию"),
    BotCommand(command="/updatecategoryname", description="Изменить наименование категории"),
    BotCommand(command="/updateprice", description="Изменить цену товара"),
    BotCommand(command="/updatephoto", description="Изменить фото товара"),
    BotCommand(command="/updatedescription", description="Изменить описание товара"),
    BotCommand(command="/updatetitle", description="Изменить название товара"),
    BotCommand(command="/updatecategory", description="Изменить категорию товара"),
]