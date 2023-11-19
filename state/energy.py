from aiogram.fsm.state import State, StatesGroup


class Energy(StatesGroup):
    GET_TITLE = State()
    GET_COUNT = State()
    GET_PRICE = State()
    GET_DESCRIPTION = State()
    CHANGE_TITLE = State()
    CHANGE_COUNT = State()
    CHANGE_PRICE = State()
    CHANGE_DESCRIPTION = State()
    GET_ID = State()


class BuyEnergy(StatesGroup):
    GET_COUNT = State()
    GET_ROOM = State()
    GET_TITLE = State()
