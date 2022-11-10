from aiogram.dispatcher.filters.state import StatesGroup, State


class Survey(StatesGroup):
    FIO = State()
    Age = State()
    Height = State()
    Bust = State()
    Waist = State()
    Hips = State()
    Size = State()
    Leg_size = State()
    Disk = State()


class Prolong(StatesGroup):
    F1 = State()
    F2 = State()
    P = State()
    D = State()

class NewPost(StatesGroup):
    EnterMessage = State()
    EnterPhoto = State()
    When = State()
    Channel = State()
    Confirm = State()
    Final = State()


class DataState(StatesGroup):
    One = State()


class SuperAdmin(StatesGroup):
    AddAdmin = State()
    DeleteAdmin = State()