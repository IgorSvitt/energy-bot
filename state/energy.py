from aiogram.fsm.state import State, StatesGroup


class Good(StatesGroup):
    GET_ID = State()
    GET_TITLE = State()
    GET_COUNT = State()
    GET_PRICE = State()
    GET_PHOTO = State()
    GET_DESCRIPTION = State()
    CHANGE_TITLE = State()
    CHANGE_COUNT = State()
    CHANGE_PRICE = State()
    CHANGE_DESCRIPTION = State()
    CHANGE_PHOTO = State()
    GET_CATEGORYID = State()


class DeleteGood(StatesGroup):
    GET_ID = State()


class UpdateGood(StatesGroup):
    GET_ID = State()
    GET_TITLE = State()
    GET_COUNT = State()
    GET_PRICE = State()
    GET_DESCRIPTION = State()
    GET_PHOTO = State()


class UpdateCountGood(StatesGroup):
    GET_ID = State()
    GET_COUNT = State()


class BuyGood(StatesGroup):
    GET_TITLE = State()
    GET_COUNT = State()
    GET_ROOM = State()


class Mailing(StatesGroup):
    GET_TEXT = State()
    GET_PHOTO = State()


class Category(StatesGroup):
    GET_TITLE = State()


class DeleteCategory(StatesGroup):
    GET_ID = State()
