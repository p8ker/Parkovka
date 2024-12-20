from aiogram.fsm.state import StatesGroup, State

class Wait(StatesGroup):
    number = State()

class TimeUser(StatesGroup):
    timeForWait = State()
    timeToAnswer = State()