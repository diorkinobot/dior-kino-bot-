import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- SIZNING MA'LUMOTLARINGIZ ---
API_TOKEN = '8734980908:AAEv6vKzRaVWEGMmkZ4QigssOEh4seNEt0A'
ADMIN_ID = 5574075754

# Majburiy kanallar ro'yxati (ID yoki username)
# Eslatma: Maxfiy kanallar uchun ularning ID raqami ishlatiladi
CHANNELS = ['@diorkino_kodi', -1002084534567, -1002154321098] # Namuna sifatida ID qo'yildi

# Kanallarga havola (Tugmalar uchun)
CHANNEL_LINKS = [
    "https://t.me/diorkino_kodi",
    "https://t.me/+D7iHwkMWsow5OWQy",
    "https://t.me/+WXNSgddxFKk0ZWYy"
]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def check_sub(user_id):
    for i, channel in enumerate(CHANNELS):
        try:
            # Agar username bo'lsa username, aks holda link orqali tekshirish murakkabroq
            # Shuning uchun bot barcha kanallarda ADMIN bo'lishi shart!
            member = await bot.get_chat_member(chat_id=channel if isinstance(channel, int) else channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except Exception:
            # Bot admin bo'lmasa yoki kanal topilmasa bu yerda xato berishi mumkin
            continue 
    return True

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    if await check_sub(message.from_user.id):
        await message.answer("Xush kelibsiz! Kino kodini yuboring 🍿")
    else:
        buttons = []
        for i, link in enumerate(CHANNEL_LINKS):
            buttons.append([InlineKeyboardButton(text=f"{i+1}-kanalga a'zo bo'lish ➕", url=link)])
        
        buttons.append([InlineKeyboardButton(text="Tasdiqlash ✅", callback_data="check")])
        
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer("Botdan foydalanish uchun barcha kanallarga obuna bo'ling:", reply_markup=markup)

@dp.callback_query(F.data == "check")
async def check_callback(call: types.CallbackQuery):
    if await check_sub(call.from_user.id):
        await call.message.delete()
        await call.message.answer("Obuna tasdiqlandi! Kino kodini yuboring 🍿")
    else:
        await call.answer("Hali hamma kanallarga a'zo emassiz! ❌", show_alert=True)

@dp.message(F.text)
async def movie_handler(message: types.Message):
    if not await check_sub(message.from_user.id):
        await start_handler(message)
        return

    # KINO BAZASI
    db = {
        "1": "🎬 Film: 'Qasoskorlar'\n🔗 Link: https://t.me/diorkino_kodi/5",
    }

    code = message.text
    if code in db:
        await message.answer(db[code])
    else:
        await message.answer("Bunday kodli kino topilmadi ❌")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
