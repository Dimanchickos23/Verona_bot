from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

chat_cb = CallbackData('chat', 'chat_id', 'chat_name', 'action')

end_survey = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📝 Выслать данные", callback_data="survey_end")
    ],
    [
        InlineKeyboardButton(text="🆘 В анкете ошибка!", callback_data="error")
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
# Test_channel_id=-1001816253590      Girls=-1001657141038
channels_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Girls", callback_data="-1001816253590"),
            InlineKeyboardButton(text="GUYS", callback_data="-1001682352777"),
        ],
        [
            InlineKeyboardButton(text="KIDS", callback_data="-1001553289773"),
            InlineKeyboardButton(text="PLUS_SIZE", callback_data="-1001503006255"),
        ],
        [
            InlineKeyboardButton(text="Girls 35+", callback_data="-1001616464016")
        ]
    ]
)

channel_cb = CallbackData('post', 'action', 'id', 'name')
