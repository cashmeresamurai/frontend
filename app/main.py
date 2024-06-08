from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, Header, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.backend_json import register_user

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit", response_class=HTMLResponse)
async def submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    hx_request: Optional[str] = Header(None),
):
    print(f"Received email: {email}, password: {password}")
    register_new_user = register_user(email=email, password=password)
    if register_new_user:
        print("User registered successfully.")
        return RedirectResponse(
            url=f"/confirm_email?email={email}", status_code=303
        )
    else:
        print("User registration failed.")
        return templates.TemplateResponse(
            "components/error_register.html", {"request": request}, status_code=400
        )

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})
