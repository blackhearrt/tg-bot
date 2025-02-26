import asyncio
import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from aiogram import Bot, Dispatcher, types, Router, F, html
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode



load_dotenv() 
BOT_TOKEN = os.getenv("BOT_TOKEN")
TOKEN = BOT_TOKEN

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def currency_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [InlineKeyboardButton(text="💵 USD", callback_data="currency_usd")],
            [InlineKeyboardButton(text="💴 EUR", callback_data="currency_eur")],
            [InlineKeyboardButton(text="🇵🇱 PLN", callback_data="currency_pln")]
        ]
    )
    return keyboard

@dp.message(Command("start"))
async def start_cmd(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "📊 Курс валют")],
            [KeyboardButton(text = "✅ TODO-ліст")],
            [KeyboardButton(text = "Головне меню")]
        ],
        resize_keyboard = True
    )
    await message.answer("Виберіть функцію:", reply_markup = keyboard)

@dp.message(F.text =="📊 Курс валют")
async def currency(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "💲 Отримати курс валюти")],
            [KeyboardButton(text = "⬅ Назад")]
        ],
        resize_keyboard = True
    )
    await message.answer("Виберіть функцію:", reply_markup = keyboard)

@dp.message(F.text == "💲 Отримати курс валюти")
async def show_currency_menu(message: types.Message):
    await message.answer("Оберіть валюту:", reply_markup=currency_keyboard())

@dp.callback_query(F.data.startswith("currency_"))    
async def get_currency(callback: types.CallbackQuery):
   
    currency_code = callback.data.split("_")[1].upper()

    currency_map = {
        840: "USD",  # Долар США
        978: "EUR",  # Євро
        985: "PLN",  # Польський злотий
    }

    if currency_code not in currency_map.values():
        await callback.answer("❌ Невідома валюта")
        return

    url = "https://api.monobank.ua/bank/currency"
    response = requests.get(url)

    if response.status_code != 200:
        await callback.message.answer("❌ Не вдалося отримати курс валют. Спробуйте пізніше.")
        return
    
    data = response.json()

    for item in data:
        if item["currencyCodeA"] in currency_map and item["currencyCodeB"] == 980:  # UAH
            rate_buy = item.get("rateBuy", "❌ Немає даних") 
            rate_sell = item.get("rateSell", "❌ Немає даних")

            message_text = f"💱 <b>Курс {currency_code} станом на {now}</b>\n\n"
            message_text += f"<b>{currency_code}:</b> Купівля: {rate_buy} | Продаж: {rate_sell}"           

        await callback.message.answer(message_text, parse_mode="HTML")
        return
    await callback.message.answer("❌ Курс не знайдено.")

@dp.message(F.text == "✅ TODO-ліст")
async def todo_keyboard(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "✍📋Список справ")],
            [KeyboardButton(text = "⬅ Назад")]
        ],
        resize_keyboard = True
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
        resize_keyboard = True
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

