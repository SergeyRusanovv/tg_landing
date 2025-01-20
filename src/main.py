from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config import AppConfig

import smtplib
from email.message import EmailMessage


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


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
    send_email = EmailMessage()
    send_email["Subject"] = "Здравствуйте"
    send_email["From"] = AppConfig.SMTP_USER
    send_email["To"] = email
    send_email['Disposition-Notification-To'] = AppConfig.SMTP_USER

    phone_number = phone if phone else "Вы не указали ваш номер телефона"
    telegram_url = telegram if telegram else "Вы не указали ссылку на телеграмм"

    send_email.set_content(
        "<div>"
        f'<h1 style="color: red;">Здравствуйте! {first_name} {last_name} 😊</h1><p>Ваши данные из рекламы получены. '
        f'Email: {email}, Телефон: {phone_number}, Ссылка в телеграмм: {telegram_url}</p></div>',
        subtype="html",
    )

    with smtplib.SMTP_SSL(AppConfig.SMTP_HOST, AppConfig.SMTP_PORT) as server:
        server.login(AppConfig.SMTP_USER, AppConfig.SMTP_PASSWORD)
        server.send_message(send_email)

    return {"message": "Уведомления отправлены!"}
