import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="🍔 Еда"), types.KeyboardButton(text="🛒 Маркетплейсы")],
        [types.KeyboardButton(text="💊 Аптеки"), types.KeyboardButton(text="👕 Одежда")],
        [types.KeyboardButton(text="📱 Техника"), types.KeyboardButton(text="⭐ Все акции")]
    ],
    resize_keyboard=True
)

def load_data():
    with open("data.json", "r", encoding="utf-8") as f:
        return json.load(f)

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "💸 CashBackBot\n\nВыбирай категорию и получай акции 👇",
        reply_markup=keyboard
    )

@dp.message()
async def handle(message: types.Message):
    data = load_data()

    mapping = {
        "🍔 Еда": "food",
        "🛒 Маркетплейсы": "market"
    }

    if message.text in mapping:
        items = data.get(mapping[message.text], [])
        for item in items:
            await message.answer(
                f"<b>{item['title']}</b>\n"
                f"{item['text']}\n"
                f"Промокод: <code>{item['code']}</code>\n"
                f"<a href='{item['link']}'>Перейти</a>",
                parse_mode="HTML"
            )
    else:
        await message.answer("Выбери категорию кнопками 👇")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
