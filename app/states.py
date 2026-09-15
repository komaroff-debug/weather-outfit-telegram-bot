from aiogram.fsm.state import State, StatesGroup

class UserStates(StatesGroup):
    waiting_for_city = State()
    choosing_city = State()
    waiting_for_notification_time = State()
