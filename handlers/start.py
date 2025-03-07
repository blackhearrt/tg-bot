from aiogram import Router, types
from aiogram.filters import Command
from utils.helpers import get_greeting, get_time_info
from keyboards import main_keyboard

router = Router()

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    greeting = get_greeting()
    time_info = get_time_info()
    username = message.from_user.full_name or "шановний"
    
    await message.answer(
        f"📅 {time_info}\n\n"
        f"👋 {greeting}, {username}! Які плани на сьогодні?\n\n", 
        reply_markup=main_keyboard
    )

