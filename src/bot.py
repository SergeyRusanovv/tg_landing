import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from config import AppConfig


bot = Bot(token=AppConfig.BOT_TOKEN.get_secret_value())
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Открыть лендинг...', web_app=WebAppInfo(url=AppConfig.WEBAPP_URL))]
    ])
    await message.answer("Hello!", reply_markup=markup)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
