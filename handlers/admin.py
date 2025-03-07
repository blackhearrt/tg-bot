from aiogram import Router, types
from aiogram.filters import Command
from utils.database import load_admins, save_admins

router = Router()
ADMIN_IDS = load_admins()

@router.message(Command("addadmin"))
async def add_admin(message: types.Message):
    global ADMIN_IDS
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас немає прав!")
        return
    
    try:
        new_admin_id = int(message.text.split()[1])
        if new_admin_id in ADMIN_IDS:
            await message.answer("✅ Користувач вже є адміністратором.")
            return

        ADMIN_IDS.add(new_admin_id)
        save_admins(ADMIN_IDS)
        await message.answer(f"✅ {new_admin_id} доданий.")
    except (IndexError, ValueError):
        await message.answer("❌ Вкажіть ID!")

@router.message(Command("removeadmin"))
async def remove_admin(message: types.Message):
    global ADMIN_IDS
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас немає прав для цієї команди!")
        return

    try:
        admin_id = int(message.text.split()[1])
        if admin_id not in ADMIN_IDS:
            await message.answer("❌ Цей користувач не є адміністратором.")
            return

        ADMIN_IDS.remove(admin_id)
        save_admins(ADMIN_IDS)
        await message.answer(f"❌ Користувач {admin_id} видалений з адміністраторів.")
    except (IndexError, ValueError):
        await message.answer("❌ Вкажіть правильний ID користувача! Наприклад: /removeadmin 123456789")

@router.message(Command("admins"))
async def show_admins(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("❌ У вас немає прав для цієї команди!")
        return
    
    if not ADMIN_IDS:
        await message.answer("ℹ Список адміністраторів порожній.")
    else:
        admins_list = "\n".join([f"🔹 {admin_id}" for admin_id in ADMIN_IDS])
        await message.answer(f"📋 <b>Список адміністраторів:</b>\n{admins_list}", parse_mode="HTML")
