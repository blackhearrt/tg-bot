from aiogram import types, Router, Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import F
import asyncio
from datetime import datetime

router = Router()

# Клавіатура головного меню трекера завдань
@router.message(F.text == "✅ Трекер завдань")
async def todo_keyboard(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Переглянути списки")],
            [KeyboardButton(text="✍ Додати нове завдання")],
            [KeyboardButton(text="⏰ Дедлайни та нагадування")],
            [KeyboardButton(text="⬅ Назад")]
        ],
        resize_keyboard=True
    )
    
    welcome_text = (
        "📝 <b>Ласкаво просимо до персонального трекера!</b>\n\n"
        "Тут Ви можете керувати своїми списками справ:\n"
        "📋 Переглянути та редагувати списки\n"
        "✍ Додати нове завдання\n"
        "⏰ Встановити нагадування\n\n"
        "Виберіть дію:"
    )
    await message.answer(welcome_text, parse_mode="HTML", reply_markup=keyboard)

# Стан для створення завдань
class TaskCreation(StatesGroup):
    choosing_list = State()
    entering_task = State()

# 📋 Переглянути списки
@router.message(F.text == "📋 Переглянути списки")
async def view_task_lists(message: types.Message):
    task_lists = ["Робота", "Навчання", "Особисте"]  # Пізніше заміниться на БД
    
    if not task_lists:
        await message.answer("❌ У вас поки немає списків завдань.")
        return
    
    lists_text = "📂 <b>Ваші списки:</b>\n\n" + "\n".join([f"📌 {lst}" for lst in task_lists])
    await message.answer(lists_text, parse_mode="HTML")

# ✍ Додати нове завдання
@router.message(F.text == "✍ Додати нове завдання")
async def add_task_start(message: types.Message, state: FSMContext):
    await state.set_state(TaskCreation.choosing_list)
    await message.answer("📂 Введіть назву списку, до якого додати завдання:")

@router.message(TaskCreation.choosing_list)
async def add_task_choose_list(message: types.Message, state: FSMContext):
    await state.update_data(task_list=message.text)
    await state.set_state(TaskCreation.entering_task)
    await message.answer("📝 Введіть текст завдання:")

@router.message(TaskCreation.entering_task)
async def add_task_enter_task(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task_list = data.get("task_list")
    task_text = message.text
    
    await message.answer(f"✅ Завдання додано до списку <b>{task_list}</b>:\n📌 {task_text}", parse_mode="HTML")
    await state.clear()

# ⏰ Дедлайни та нагадування
@router.message(F.text == "⏰ Дедлайни та нагадування")
async def reminders_menu(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Переглянути нагадування")],
            [KeyboardButton(text="⏰ Додати нагадування")],
            [KeyboardButton(text="⬅ Назад")]
        ],
        resize_keyboard=True
    )
    await message.answer("🔔 Виберіть функцію:", parse_mode="HTML", reply_markup=keyboard)

reminders = []

@router.message(F.text == "⏰ Додати нагадування")
async def add_reminder_start(message: types.Message, state: FSMContext):
    await state.set_state(TaskCreation.entering_task)
    await message.answer("📅 Введіть дату та час нагадування (формат: РРРР-ММ-ДД ГГ:ХХ):")

@router.message(TaskCreation.entering_task)
async def add_reminder_time(message: types.Message, state: FSMContext):
    try:
        reminder_time = datetime.strptime(message.text, "%Y-%m-%d %H:%M")
        if reminder_time < datetime.now():
            await message.answer("❌ Дата у минулому! Введіть правильний час.")
            return
        await state.update_data(reminder_time=reminder_time)
        await state.set_state(TaskCreation.choosing_list)
        await message.answer("📝 Введіть текст нагадування:")
    except ValueError:
        await message.answer("❌ Невірний формат! Введіть у форматі: РРРР-ММ-ДД ГГ:ХХ")

@router.message(TaskCreation.choosing_list)
async def add_reminder_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    reminder_time = data["reminder_time"]
    
    reminder = {
        "user_id": message.from_user.id,
        "time": reminder_time,
        "text": message.text
    }
    reminders.append(reminder)
    
    await message.answer(f"✅ Нагадування збережено! 📅 {reminder_time.strftime('%Y-%m-%d %H:%M')}\n🔔 {message.text}")
    await state.clear()

async def reminder_checker(bot: Bot):
    while True:
        now = datetime.now()
        for reminder in reminders[:]:
            if reminder["time"] <= now:
                await bot.send_message(reminder["user_id"], f"🔔 <b>Нагадування!</b>\n\n{reminder['text']}", parse_mode="HTML")
                reminders.remove(reminder)
        await asyncio.sleep(30)

async def on_startup():
    asyncio.create_task(reminder_checker())
