import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message, Update, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import AsyncGenerator

from config import AppConfig


async def lifespan(app: FastAPI) -> AsyncGenerator:
    yield
    await bot.session.close()


bot = Bot(token=AppConfig.BOT_TOKEN.get_secret_value())
dp = Dispatcher()

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@dp.message(CommandStart())
async def start(message: Message) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Открыть лендинг...', web_app=WebAppInfo(url=AppConfig.WEBAPP_URL))]
    ])
    await message.answer("Hello!", reply_markup=markup)


@app.get(path="/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit")
async def submit(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    telegram: str = Form(None)
):
    return {"message": "Форма успешно отправлена!", "data": {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "telegram": telegram
    }}


async def start_bot():
    print("Бот полетел")
    await dp.start_polling(bot)


async def start_fastapi():
    print("Веб полетел")
    import uvicorn
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await asyncio.gather(start_bot(), start_fastapi())


if __name__ == "__main__":
    asyncio.run(main())
