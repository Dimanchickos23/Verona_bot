from aiogram import types

start_survey = [
    [
        types.KeyboardButton(text="📝 Заполнить анкету")
    ]
]

survey_markup = types.ReplyKeyboardMarkup(
    keyboard=start_survey,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Нажмите")
