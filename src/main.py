from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


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
    return {"message": "Форма успешно отправлена!", "data": {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "telegram": telegram
    }}
