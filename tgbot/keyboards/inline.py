from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

survey_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📝 Заполнить анкету", callback_data="survey_start")
    ]
])

end_survey = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📝 Выслать данные", callback_data="survey_end")
    ]
])

url = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Материалы", url="https://vmodel.ru/qr/")
    ]
])

prolong_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Продлить контракт", url="https://vmodel.ru/qr/")
    ],
    [
        InlineKeyboardButton(text="Завершить сотрудничество", callback_data="contract_end")
    ]
])

post_callback = CallbackData('create_post', 'action')

confirmation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Опубликовать пост", callback_data=post_callback.new(action="post")),
        InlineKeyboardButton(text="Отклонить пост", callback_data=post_callback.new(action="cancel")),
    ]]
)

