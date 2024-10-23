import uvicorn

from fastapi import FastAPI, Depends, HTTPException, status, Security, Form
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from sources.frontend import renderer


class User(BaseModel):
    username: str
    password: str


class SingletonNoArgs(type):
    _instances = {}

    def __call__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonNoArgs, cls).__call__()
        return cls._instances[cls]


class FakeUsersDatabase(metaclass=SingletonNoArgs):
    def __init__(self, ):
        self.users = [
            User(username='admin@mail.ru', password='123'),
            User(username='sychev@mail.ru', password='456')
        ]

    def add_user(self, user: User):
        self.users.append(user)

    def get_user(self, username: str, password: str) -> User | None:
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None


#  создать экземпляр класса для выпуска jwt-токенов
access_security = JwtAccessBearer(secret_key="very_secret_key")


#  если юзер есть в бд, то выпустить токен
def login_user(user: User, db: FakeUsersDatabase = Depends(FakeUsersDatabase)) -> str:
    user_in_db = db.get_user(user.username, user.password)
    if user_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return access_security.create_access_token(subject=user_in_db.model_dump())


#  разбирает заголовки запроса и смотрит есть ли в нем jwt данные пользователя
def get_current_user(credentials: JwtAuthorizationCredentials = Security(access_security)):
    print(f'*** {credentials.subject}')
    return credentials.subject


def login_required(user: User = Depends(get_current_user)) -> User:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_renderer():
    return renderer.render('main.html')


@app.get("/login_page", response_class=HTMLResponse)
async def read_renderer():
    return renderer.render('login.html')


#  выпускает jwt - токен, если есть учетная запись пользователя
@app.post("/login")
def login(token: str = Depends(login_user)) -> str:
    return token


@app.post("/login_in", response_class=HTMLResponse)
async def login_in(email: str = Form(...),
                   password: str = Form(...), remember_me: bool = Form(False),
                   db: FakeUsersDatabase = Depends(FakeUsersDatabase),
                   ):
    user: User = User(username=email, password=password)
    print(f'user: {user}')

    user_in_db = db.get_user(user.username, user.password)
    print(f'user_in_db: {user_in_db}')

    if user_in_db is None:
        db.add_user(user)
        print(f'users: {db.users}')
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect username or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
        return renderer.render('login_result_create_new.html')
    else:
        return renderer.render('login_result_positive.html')
    # return access_security.create_access_token(subject=user_in_db.model_dump())

    # token: str = Depends(login_user)
    # return token


@app.post("/register")
def register(user: User,
             db: FakeUsersDatabase = Depends(FakeUsersDatabase),):
    db.add_user(user)
    return user


@app.get("/all_users")
def all_users(db: FakeUsersDatabase = Depends(FakeUsersDatabase)):
    return db.users


@app.get("/protected")
def protected_route(
        user: User = Depends(login_required),
        db: FakeUsersDatabase = Depends(FakeUsersDatabase),
):
    return user, db.users


@app.delete("/delete_user")
def delete_user(
        user: User = Depends(login_required),
        db: FakeUsersDatabase = Depends(FakeUsersDatabase),
):
    for u in db.users:
        if u.username == user['username']:
            db.users.remove(u)
    return f"{user} удален",


if __name__ == "__main__":
    uvicorn.run(app, port=8001)
