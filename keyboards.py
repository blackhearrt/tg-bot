from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Курс валют")],
        [KeyboardButton(text="✅ Трекер завдань")],
        [KeyboardButton(text="🏠 Головне меню")]
    ],
    resize_keyboard=True
)
