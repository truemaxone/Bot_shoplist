from aiogram.dispatcher.filters.state import State, StatesGroup


class AdditionalStep(StatesGroup):
    add_next_message = State()
    delete_next_message = State()