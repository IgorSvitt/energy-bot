from aiogram.fsm.state import State, StatesGroup


class Energy(StatesGroup):
    GET_TITLE = State()
    GET_COUNT = State()
    GET_PRICE = State()
    GET_PHOTO = State()
    GET_DESCRIPTION = State()
    CHANGE_TITLE = State()
    CHANGE_COUNT = State()
    CHANGE_PRICE = State()
    CHANGE_DESCRIPTION = State()
    GET_ID = State()


class DeleteEnergy(StatesGroup):
    GET_ID = State()


class UpdateEnergy(StatesGroup):
    GET_ID = State()
    GET_TITLE = State()
    GET_COUNT = State()
    GET_PRICE = State()
    GET_DESCRIPTION = State()
    GET_PHOTO = State()


class UpdateCountEnergy(StatesGroup):
    GET_ID = State()
    GET_COUNT = State()


class BuyEnergy(StatesGroup):
    GET_COUNT = State()
    GET_ROOM = State()
    GET_TITLE = State()


class Mailing(StatesGroup):
    GET_TEXT = State()
    GET_PHOTO = State()
