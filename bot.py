from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
import asyncio
import os
from dotenv import load_dotenv

load_dotenv() 
BOT_TOKEN = os.getenv("BOT_TOKEN")
TOKEN = BOT_TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

@dp.message(Command('start'))
async def start_cmd(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "📊 Курс валют")],
            [KeyboardButton(text = "✅ TODO-ліст")],
            [KeyboardButton(text = "Головне меню")]
        ],
        resize_keyboard= True
    )
    await message.answer("Виберіть функцію:", reply_markup = keyboard)

@dp.message(F.text =="📊 Курс валют")
async def currency_keyboard(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "💲 Отримати курс валют")],
            [KeyboardButton(text = "⬅ Назад")]
        ],
        resize_keyboard= True
    )
    await message.answer("Виберіть функцію:", reply_markup = keyboard)

@dp.message(F.text == "✅ TODO-ліст")
async def todo_keyboard(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "Список справ")],
            [KeyboardButton(text = "⬅ Назад")]
        ],
        resize_keyboard= True
    )
    await message.answer("Виберіть функцію:", reply_markup = keyboard)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())