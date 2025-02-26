import asyncio
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from aiogram import Bot, Dispatcher, types, Router, F, html
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.enums import ParseMode



load_dotenv() 
BOT_TOKEN = os.getenv("BOT_TOKEN")
TOKEN = BOT_TOKEN

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    url = "https://api.monobank.ua/bank/currency"
    response = requests.get(url)

    if response.status_code != 200:
        await message.answer("❌ Не вдалося отримати курс валют. Спробуйте пізніше.")
        return
    
    data = response.json()

    currency_map = {
        840: "USD",  # Долар США
        978: "EUR",  # Євро
        985: "PLN",  # Польський злотий
    }

    message_text = f"💱 <b>Курс валют станом на {now}</b>\n\n"
    for item in data:
        if item["currencyCodeA"] in currency_map and item["currencyCodeB"] == 980:  # UAH
            currency_name = currency_map[item["currencyCodeA"]]
            rate_buy = item.get("rateBuy", "❌ Немає даних")
            rate_sell = item.get("rateSell", "❌ Немає даних")
            message_text += f"<b>{currency_name}:</b> Купівля: {rate_buy} | Продаж: {rate_sell}\n"

    await message.answer(message_text, parse_mode="HTML")


@dp.message(F.text == "✅ TODO-ліст")
async def todo_keyboard(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "✍📋Список справ")],
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
            [KeyboardButton(text = "🏠 Головне меню")]
        ],
        resize_keyboard= True
    )
    await message.answer("Виберіть функцію:", reply_markup = keyboard)

@dp.message(F.text == "🏠 Головне меню")
async def main_menu(message: types.Message):
    username = message.from_user.full_name or "шановний"
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "📊 Курс валют")],
            [KeyboardButton(text = "✅ TODO-ліст")],
            [KeyboardButton(text = "🏠 Головне меню")]
        ],
        resize_keyboard= True
    )
    await message.answer(f"Доброго дня, {html.bold(username)}! Які плани на сьогодні?", reply_markup = keyboard)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

