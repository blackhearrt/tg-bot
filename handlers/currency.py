from aiogram import types, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import requests
from datetime import datetime

router = Router()

@router.message(Command("currency"))
@router.message(lambda message: message.text == "📊 Курс валют")
async def currency(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💲 Отримати курс валюти")],
            [KeyboardButton(text="⬅ Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("Виберіть функцію:", reply_markup=keyboard)

@router.message(lambda message: message.text == "💲 Отримати курс валюти")
async def show_currency_menu(message: types.Message):
    await message.answer("Оберіть валюту:", reply_markup=currency_keyboard())

def currency_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💵 USD", callback_data="currency_usd")],
            [InlineKeyboardButton(text="💴 EUR", callback_data="currency_eur")],
            [InlineKeyboardButton(text="🇵🇱 PLN", callback_data="currency_pln")],
            [InlineKeyboardButton(text="🇬🇧 GBP", callback_data="currency_gbp")]
        ]
    )
    return keyboard

@router.callback_query(lambda c: c.data.startswith("currency_"))
async def get_currency(callback: types.CallbackQuery):
    currency_code = callback.data.split("_")[1].upper()

    currency_map = {
        840: "USD",  # Долар США
        978: "EUR",  # Євро
        985: "PLN",  # Польський злотий
        826: "GBP"  # Фунт британський      
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
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    for item in data:
        if item["currencyCodeA"] in currency_map and item["currencyCodeB"] == 980:  # UAH
            if currency_map[item["currencyCodeA"]] == currency_code: 
                rate_buy = item.get("rateBuy", "❌ Немає даних") 
                rate_sell = item.get("rateSell", "❌ Немає даних")
                if isinstance(rate_buy, (int, float)):
                    rate_buy = round(rate_buy, 2)
                if isinstance(rate_sell, (int, float)):
                    rate_sell = round(rate_sell, 2)

                message_text = (
                    f"💱 <b>Курс {currency_code} станом на {now}</b>\n\n"
                    f"<b>{currency_code}:</b> Купівля: {rate_buy} грн | Продаж: {rate_sell} грн"
                )

                if rate_buy == "❌ Немає даних" or rate_sell == "❌ Немає даних":
                    rate_cross = item.get("rateCross", "❌ Немає даних")
                    if isinstance(rate_cross, (int, float)):
                        rate_cross = round(rate_cross, 2)
                    message_text = (
                        f"💱 <b>Курс {currency_code} станом на {now}</b>\n\n"
                        f"<b>{currency_code}:</b> {rate_cross} грн"
                    )

                await callback.message.answer(message_text, parse_mode="HTML")
                return 

    await callback.message.answer("❌ Курс не знайдено.")