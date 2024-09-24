import uvicorn

from fastapi import FastAPI, Depends, HTTPException, status, Security, Form
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials
from fastapi.responses import HTMLResponse
from fastapi_users import fastapi_users, FastAPIUsers

from auth_users import renderer
from auth_users.auth_jwt import auth_backend
from auth_users.database import User
from auth_users.manager import get_user_manager
from auth_users.schemas import UserRead, UserCreate

# from models import (User, )
app = FastAPI(title="Pet Birth Checker")

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/", response_class=HTMLResponse)
async def read_renderer():
    return renderer.render('main.html')


@app.get("/login_page", response_class=HTMLResponse)
async def read_renderer():
    return renderer.render('login.html')


current_user = fastapi_users.current_user()
@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"