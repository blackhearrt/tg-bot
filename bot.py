from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
import asyncio
import os
import requests
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
            [KeyboardButton(text = "💲 Отримати курс валюти")],
            [KeyboardButton(text = "⬅ Назад")]
        ],
        resize_keyboard= True
    )
    await message.answer("Виберіть функцію:", reply_markup = keyboard)

@dp.message(F.text == "💲 Отримати курс валюти")
async def get_currency(message: types.Message):
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    response = requests.get(url)

    if response.status_code != 200:
        await message.answer("❌ Не вдалося отримати курс валют. Спробуйте пізніше.")
        return
    data = response.json()

    currency_codes = ["USD", "EUR", "GBP", "PLN"]
    currency_data = [currency for currency in data if currency["cc"] in currency_codes]

    message_text = "💱 *Курс валют НБУ:*\n\n"
    for currency in currency_data:
         message_text += f"<b>{currency['txt']} ({currency['cc']}):</b> {currency['rate']} грн\n"

    await message.answer(message_text, parse_mode="HTML")


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

@dp.message(F.text == "⬅ Назад")
async def back(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "📊 Курс валют")],
            [KeyboardButton(text = "✅ TODO-ліст")],
            [KeyboardButton(text = "Головне меню")]
        ],
        resize_keyboard= True
    )
    await message.answer("Виберіть функцію:", reply_markup = keyboard)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

