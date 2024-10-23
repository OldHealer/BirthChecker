# from multiprocessing.pool import worker

from sqlalchemy import Integer, and_, cast, func, insert, inspect, or_, select, text, update
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload
from sqlalchemy.orm.sync import update

from ..database import engine_async, engine, Base, async_session_factory, session_factory
from ..models import UsersTable, User, PersonalData


class AsyncORM:

    @staticmethod
    async def create_tables_async():
        async with engine_async.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def insert_user_declarative_async(add_user: User):
        add_users = UsersTable(username=add_user.username, email=add_user.email)
        async with async_session_factory() as session:
            session.add_all([add_users])
            await session.flush()
            await session.commit()

    @staticmethod
    async def select_all_users():
        async with async_session_factory() as session:
            query = select(UsersTable)  # запрос всех юзеров

            # query = select(PersonalData)
            result = await session.execute(query)
            workers = result.scalars().all()  # first()
            print(f"{workers}")

            for worker in workers:
                print(f'{worker.id} - {worker.username} - {worker.email}')
            return workers

    @staticmethod
    async def update_user(user_id: int, new_value: str):
        async with async_session_factory() as session:

            worker = await session.get(UsersTable, user_id)
            worker.username = new_value
            session.add(worker)
            await session.commit()


class SyncORM:

    @staticmethod
    def insert_user(add_user: User):
        add_users = UsersTable(username=add_user.username, email=add_user.email)

        with session_factory() as session:
            session.add_all([add_users])
            session.commit()

    @staticmethod
    def select_all():
        ...