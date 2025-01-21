import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, Update
from aiogram.filters import CommandStart

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import smtplib
from email.message import EmailMessage
from config import AppConfig


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
bot = Bot(token=AppConfig.BOT_TOKEN.get_secret_value())
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message) -> None:
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Открыть лендинг...', web_app=WebAppInfo(url=AppConfig.WEBAPP_URL))]
    ])
    await message.answer("Hello!", reply_markup=markup)


@app.get(path="/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post(path="/submit")
async def submit(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(None),
    telegram: str = Form(None),
):

    send_email = EmailMessage()
    send_email["Subject"] = "Здравствуйте"
    send_email["From"] = AppConfig.SMTP_USER
    send_email["To"] = email
    send_email['Disposition-Notification-To'] = AppConfig.SMTP_USER

    phone_number = phone if phone else "Вы не указали ваш номер телефона"
    telegram_url = telegram if telegram else "Вы не указали ссылку на телеграмм"

    await bot.send_message(
        chat_id=AppConfig.TG_CHAT_ID,
        text=f"Имя: {first_name}\nФамилия: {last_name}\nEmail: {email}\nTelegram url: {telegram_url}\nНомер телефона: {phone_number}"
    )

    send_email.set_content(
        "<div>"
        f'<h1 style="color: red;">Здравствуйте! {first_name} {last_name} 😊</h1><p>Ваши данные из рекламы получены. '
        f'Email: {email}, Телефон: {phone_number}, Ссылка в телеграмм: {telegram_url}</p></div>',
        subtype="html",
    )

    with smtplib.SMTP_SSL(AppConfig.SMTP_HOST, AppConfig.SMTP_PORT) as server:
        server.login(AppConfig.SMTP_USER, AppConfig.SMTP_PASSWORD)
        server.send_message(send_email)

    return templates.TemplateResponse("submit.html", {"request": request})


async def start_bot():
    print("Бот полетел")
    await dp.start_polling(bot)


async def start_web():
    print("Веб полетел")
    import uvicorn
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await asyncio.gather(start_bot(), start_web())


if __name__ == "__main__":
    asyncio.run(main())
