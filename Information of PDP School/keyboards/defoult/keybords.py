from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

menu = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True, 
    input_field_placeholder='Tanlang...',
    keyboard=[
        [KeyboardButton(text='Info📝'),KeyboardButton(text="Manzilni ko'rish📍")],
        [KeyboardButton(text="Savol yubormoqchiman✍🏻"),KeyboardButton(text="Biz bilan bog'lanish📞")],
        [KeyboardButton(text='Web Ilova', web_app=WebAppInfo(url="https://school.pdp.uz/"))]
    ]
)

menu1 = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True, 
    input_field_placeholder='Tanlang...',
    keyboard=[
        [KeyboardButton(text='Info📝'),KeyboardButton(text="Manzilni ko'rish📍")],
        [KeyboardButton(text="Savol yuborish✍🏻"),KeyboardButton(text="Biz bilan bog'lanish📞")],
        [KeyboardButton(text='Web Ilova', web_app=WebAppInfo(url="https://school.pdp.uz/"))]
    ]
)

contact = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder='Tanlang...',
    keyboard=[
        [KeyboardButton(text='Telefon raqam'), KeyboardButton(text='Web-sayt')],
        [KeyboardButton(text='Telegram'), KeyboardButton(text='Facebook')],
        [KeyboardButton(text='Instagram'),KeyboardButton(text="Asosiy menu🏠")]
    ]
)

tel = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Telefon raqamingizni jo'nating!",
    keyboard=[
        [KeyboardButton(text="Telefon raqam jo'natish📱", request_contact=True)]
    ]
)

register = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True,
    keyboard=[
        [KeyboardButton(text="Ro'yhatdan o'tish📋")]
    ]
)   

