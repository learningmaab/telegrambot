import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram import Router

# ✅ Bot tokenini o‘rnating
TOKEN = "7004338587:AAHMLrinQbLiAdip9E129MQR96pFW_UcriA"
# ✅ Obuna tekshirish uchun kanallar
CHANNELS = ["@qoqon21", "@nosirov_mn"]

# ✅ Kino ma'lumotlar bazasi
movies = {
    "232": "https://t.me/qoqon21/46",
    "101": "https://t.me/qoqon21/37",
    "7": "https://t.me/2095612288/1455"
}

# ✅ Bot va Dispatcher yaratamiz
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# ✅ Logging sozlash
logging.basicConfig(level=logging.INFO)

# ✅ Obuna tekshirish tugmalari
def check_subscription_keyboard():
    keyboard = [[InlineKeyboardButton(text=f"📢 {channel}", url=f"https://t.me/{channel[1:]}")] for channel in CHANNELS]
    keyboard.append([InlineKeyboardButton(text="✅ Obuna bo'ldim", callback_data="check_subscription")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# ✅ Obuna tekshirish funksiyasi
async def check_subscription(user_id):
    not_subscribed = []
    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                not_subscribed.append(channel)
        except Exception:
            not_subscribed.append(channel)
    return not_subscribed

# 🎬 Start komandasi (Obunani tekshiradi)
@router.message(Command("start"))
async def send_welcome(message: Message):
    user_id = message.from_user.id
    not_subscribed = await check_subscription(user_id)

    if not not_subscribed:
        await message.answer("🎬 Salom! Kinoni olish uchun raqam kiriting.")
    else:
        text = "Botdan foydalanish uchun quyidagi kanallarga obuna bo‘lishingiz kerak:"
        await message.answer(text, reply_markup=check_subscription_keyboard())

# ✅ Obuna tekshirish tugmasi bosilganda
@router.callback_query(lambda call: call.data == "check_subscription")
async def check_user_subscription(call: CallbackQuery):
    not_subscribed = await check_subscription(call.from_user.id)

    if not not_subscribed:
        await call.message.answer("✅ Siz obuna bo‘ldingiz! Kinoni olish uchun raqam kiriting.")
    else:
        text = "Siz hali quyidagi kanallarga obuna bo‘lmadingiz:\n"
        for channel in not_subscribed:
            text += f"- {channel}\n"
        await call.message.answer(text, reply_markup=check_subscription_keyboard())

    await call.answer()

# 🎥 Kino raqami yuborilganda tekshirish va yuborish
@router.message(lambda message: message.text.isdigit())
async def send_movie(message: Message):
    user_id = message.from_user.id
    not_subscribed = await check_subscription(user_id)

    if not not_subscribed:
        movie_id = message.text.strip()
        if movie_id in movies:
            video_url = movies[movie_id]
            await message.answer_video(video_url, caption=f"📽 {movie_id} raqamli kino!")
        else:
            await message.answer("😔 Kechirasiz, bu raqamga mos kino topilmadi.")
    else:
        text = "Botdan foydalanish uchun quyidagi kanallarga obuna bo‘lishingiz kerak:"
        await message.answer(text, reply_markup=check_subscription_keyboard())

# ✅ Asosiy botni ishga tushirish funksiyasi
async def main():
    await bot.delete_webhook(drop_pending_updates=True)  # Eski xabarlarni o‘chirish
    await dp.start_polling(bot)

# ✅ Botni ishga tushirish
if __name__ == "__main__":
    asyncio.run(main())
