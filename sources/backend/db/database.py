import asyncio

from sqlalchemy import create_engine, text, insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

from .models import metadata_obj, users_table, UsersTable, User, Base

#  определить синхронный движок
engine = create_engine(
    url=r'sqlite:///D:/Python_projects/pets/birth_checker/db_birth_checker.sqlite3',
    echo=True,
)
#  определить асинхронный движок
engine_async = create_async_engine(
    url=r'sqlite+aiosqlite:///D:/Python_projects/pets/birth_checker/db_birth_checker.sqlite3',
    echo=True,
)

#  создать синхронную сессию соединения с БД
session_factory = sessionmaker(engine)
#  создать асинхронную сессию соединения с БД
async_session_factory = async_sessionmaker(engine_async)


#  проверить подключение к БД (асинхронно)
async def create_async_connection():
    async with engine_async.connect() as conn:
        res = await conn.execute(text("SELECT sqlite_version();"))  # .fetchone()
        print(res.first())


#  проверить подключение к БД
def create_connection():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT sqlite_version();"))  # .fetchone()
        print(res.first())


#  добавление в БД сырым запросом
def insert_data_fresh():
    with engine.connect() as conn:
        conn.execute(text("""INSERT INTO users (username, email) VALUES 
                             ('Dmitrii', 'dmitrii@mail.com');"""))
        conn.commit()


#  добавление в БД с использованием querybuilder
stmt = insert(users_table).values(
    [
        {'username': 'name_1', 'email': 'name_1@mail.com'},
        {'username': 'name_2', 'email': 'name_2@mail.com'},
    ]
)


def insert_data(query):
    """ Cинхронный метод добавления в БД """
    with engine.connect() as conn:
        conn.execute(query)
        conn.commit()


def create_tables():
    """ Создание таблиц """
    Base.metadata.create_all(engine)


def insert_data_declarative():
    add_user = UsersTable(username='Dmitrii', email='dmitrii@mail.com')
    add_user_1 = UsersTable(username='Nailia', email='nailia@mail.com')

    with session_factory() as session:
        session.add_all([add_user, add_user_1])
        session.commit()


if __name__ == '__main__':


    # asyncio.run(create_async_connection())
    # create_connection()
    # create_tables()
    # drop_table()
    # insert_data(query=stmt)
    # asyncio.run(insert_user_declarative_async(user))
    insert_data_declarative()
