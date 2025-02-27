import asyncio
import os
import requests
import json
from pathlib import Path
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

USER_IDS_FILE = Path(__file__).parent / "user_ids.json"

def load_chat_ids():
    if not USER_IDS_FILE.exists():
        return {}  
    try:
        with open(USER_IDS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)  
    except json.JSONDecodeError:
        return {} 

def save_chat_ids(user_data):
    with open(USER_IDS_FILE, "w", encoding="utf-8") as file:
        json.dump(user_data, file, indent=4, ensure_ascii=False)

def get_time_info():
    now = datetime.now()
    days_of_week = {
        0: "Понеділок", 1: "Вівторок", 2: "Середа", 3: "Четвер",
        4: "П'ятниця", 5: "Субота", 6: "Неділя"
    }
    day_name = days_of_week[now.weekday()]
    formatted_time = now.strftime("%H:%M")
    formatted_day = now.strftime("%d.%m.%Y")

    return f"{day_name}, {formatted_time} | {formatted_day}"

def get_greeting():
   
    now = datetime.now().time()  
    
    if now >= datetime.strptime("05:01", "%H:%M").time() and now <= datetime.strptime("11:30", "%H:%M").time():
        return "Доброго ранку"
    elif now >= datetime.strptime("11:31", "%H:%M").time() and now <= datetime.strptime("16:30", "%H:%M").time():
        return "Доброго дня"
    elif now >= datetime.strptime("16:31", "%H:%M").time() and now <= datetime.strptime("23:00", "%H:%M").time():
        return "Доброго вечора"
    else:
        return "Доброї ночі"

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
            [KeyboardButton(text = "✅ TODO-ліст")],
            [KeyboardButton(text = "🏠 Головне меню")]
        ],
        resize_keyboard= True
    )
    sent_message = await message.answer(
        f"📅 {time_info}\n\n"
        f"👋 {greeting}, {html.bold(username)}! Які плани на сьогодні?\n\n", 
        reply_markup = keyboard
    )

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
            [KeyboardButton(text = "✅ TODO-ліст")],
            [KeyboardButton(text = "🏠 Головне меню")]
        ],
        resize_keyboard= True
    )
    sent_message = await message.answer(
        f"📅 {time_info}\n\n"
        f"👋 {greeting}, {html.bold(username)}! Які плани на сьогодні?\n\n", 
        reply_markup = keyboard
    )


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

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

