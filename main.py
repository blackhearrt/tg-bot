from aiogram import Bot, Dispatcher, html, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, BotCommand
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

import logging

import asyncio

from handlers import currency, todo, admin, messaging
from handlers.todo import reminder_checker
from config import BOT_TOKEN
from utils.database import save_chat_ids, load_chat_ids, load_admins
from utils.helpers import get_greeting, get_time_info

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
ADMON_IDS = load_admins()

# start
@dp.message(Command("start"))
async def start_cmd(message: Message):
    user_chat_ids = load_chat_ids()  
    user_id = str(message.chat.id)  
    username = message.from_user.username or message.from_user.full_name  
    
    user_chat_ids[user_id] = username

    save_chat_ids(user_chat_ids) 
    greeting = get_greeting()
    time_info = get_time_info()
    username = message.from_user.full_name or "шановний"
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "📊 Курс валют")],
            [KeyboardButton(text = "✅ Трекер завдань")],
            [KeyboardButton(text = "🏠 Головне меню")]
        ],
        resize_keyboard= True
    )
    sent_message = await message.answer(
        f"📅 {time_info}\n\n"
        f"👋 {greeting}, <b>{username}</b>! Які плани на сьогодні?\n\n", parse_mode="HTML",
        reply_markup = keyboard
    )

# Main menu
@dp.message(F.text == "🏠 Головне меню")
async def main_menu(message: types.Message):
    user_chat_ids = load_chat_ids()
    user_id = str(message.chat.id) 
    username = message.from_user.username or message.from_user.full_name  

    user_chat_ids[user_id] = username

    save_chat_ids(user_chat_ids)
    greeting = get_greeting()
    time_info = get_time_info()
    username = message.from_user.full_name or "шановний"
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "📊 Курс валют")],
            [KeyboardButton(text = "✅ Трекер завдань")],
            [KeyboardButton(text = "🏠 Головне меню")]
        ],
        resize_keyboard= True
    )
    sent_message = await message.answer(
        f"📅 {time_info}\n\n"
        f"👋 {greeting}, <b>{username}</b>! Які плани на сьогодні?\n\n", parse_mode="HTML",
        reply_markup = keyboard
    )

# Back menu
@dp.message(F.text == "⬅ Назад")
async def back(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "📊 Курс валют")],
            [KeyboardButton(text = "✅ Трекер завдань")],
            [KeyboardButton(text = "🏠 Головне меню")]
        ],
        resize_keyboard = True
    )
    await message.answer("Виберіть функцію:", reply_markup = keyboard)


async def main():
    logging.basicConfig(level=logging.INFO)

    
    dp.include_router(currency.router)
    dp.include_router(todo.router)
    dp.include_router(admin.router)
    dp.include_router(messaging.router)

    await bot.set_my_commands([
        BotCommand(command="start", description="Запустити бота"),
        BotCommand(command="help", description="Допомога"),
    ])

    asyncio.create_task(reminder_checker(bot))

    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())