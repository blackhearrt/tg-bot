from aiogram import Router, Bot, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


from utils.database import registered_users, save_chat_ids, ADMIN_IDS, load_admins

router = Router()

@router.message(Command("sendall"))
async def send_broadcast(message: Message, bot: Bot):
    if message.from_user.id not in load_admins():
        await message.answer("❌ У вас немає прав для цієї команди!")
        return

    text = message.text.replace("/sendall", "").strip()
    if not text:
        await message.answer("❌ Напишіть текст повідомлення після команди `/sendall`")
        return

    success_count, fail_count = 0, 0
    for user_id in list(registered_users.keys()):
        try:
            await bot.send_message(int(user_id), f"📢 <b>Оголошення:</b>\n\n{text}", parse_mode="HTML")
            success_count += 1
        except Exception as e:
            print(f"❌ Не вдалося відправити {user_id}: {e}")
            del registered_users[user_id]  
            fail_count += 1

    save_chat_ids(registered_users)
    await message.answer(f"✅ Успішно надіслано: {success_count} користувачам\n❌ Помилки: {fail_count}")

@router.message(Command("send"))
async def send_private_message(message: Message, bot: Bot):
    if message.from_user.id not in load_admins():
        await message.answer("❌ У вас немає прав для цієї команди!")
        return

    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("❌ Формат команди: `/send ID текст` або `/send @username текст`")
        return

    target, text = args[1], args[2]

    if target.isdigit():
        user_id = target
    elif target.startswith("@"):  
        user_id = next((uid for uid, uname in registered_users.items() if uname == target[1:]), None)
        if user_id is None:
            await message.answer("❌ Користувача з таким юзернеймом не знайдено.")
            return
    else:
        await message.answer("❌ Невірний формат. Використовуйте `/send ID текст` або `/send @username текст`")
        return

    try:
        await bot.send_message(int(user_id), f"⚠️ <b>{text}</b>", parse_mode="HTML")
        await message.answer("✅ Повідомлення успішно відправлено!")
    except Exception as e:
        await message.answer(f"❌ Не вдалося надіслати: {e}")