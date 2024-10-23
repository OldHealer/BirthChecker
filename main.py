import os
import sys
import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from sources.backend.db.queries.orm import AsyncORM, SyncORM
from sources.backend.db.models import User

from sources.frontend import renderer

from sources.backend.auth.auth import auth_router
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# from fastapi_users import FastAPIUsers
# from pydantic import BaseModel
#
# from frontend import renderer

# from backend.auth.auth_jwt import auth_backend
# from backend.auth.database import User
# from backend.auth.manager import get_user_manager
# from backend.auth.schemas import UserRead, UserCreate

# from models import (User, )
# app = FastAPI(title="Birth Checker")

# fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend],)
#
# app.include_router(
#     fastapi_users.get_auth_router(auth_backend),
#     prefix="/auth/jwt",
#     tags=["auth"],
# )
#
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate),
#     prefix="/auth",
#     tags=["auth"],
# )

# async def main():
#     # await AsyncORM.insert_user_declarative_async()
#     # await AsyncORM.update_user()
#     await AsyncORM.select_all_users()


app = FastAPI(title="BirthChecker")
# app.add_middleware(CORSMiddleware, allow_origins=["*"],)

app.include_router(auth_router)

@app.get("/", tags=["Стартовая страница"], response_class=HTMLResponse)
async def start_page():
    return renderer.render('main.html')


@app.get("/all_users", tags=["Все пользователи"])
async def get_all_users():
    return await AsyncORM.select_all_users()


# @app.get("/", response_class=HTMLResponse)
# async def read_renderer():
#     return renderer.render('main.html')
#
#
# @app.get("/login_page", response_class=HTMLResponse)
# async def read_renderer():
#     return renderer.render('login.html')
#
#
# current_user = fastapi_users.current_user()
# @app.get("/protected-route")
# def protected_route(user: User = Depends(current_user)):
#     return f"Hello, {user.username}"
#  TODO : прикрутить аутентификацию и использовать закрытый урл
#  TODO : добавить поля в БД


if __name__ == '__main__':
    user = User()
    user.username = 'Vadim'
    user.email = 'olga@gmail.com'

    # uvicorn.run(
    #     app="birth_checker.main:app",
    #     port=8001,
    #     reload=True,
    # )
    # SyncORM.insert_user(user)
    # asyncio.run(AsyncORM.create_tables_async())
    asyncio.run(AsyncORM.insert_user_declarative_async(user))
    # asyncio.run(AsyncORM.select_all_users())
    # asyncio.run(AsyncORM.update_user(user_id=1, new_value='DmitrII'))