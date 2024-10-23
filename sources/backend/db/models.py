import datetime

from datetime import datetime, timezone
from typing import Annotated

from sqlalchemy import (ForeignKey, MetaData, Integer, String, TIMESTAMP, Table, Column, JSON, Boolean, text)
from sqlalchemy.orm import (Mapped, mapped_column, Session, sessionmaker, DeclarativeBase)

metadata_obj = MetaData()


class Base(DeclarativeBase):
    pass


class User:
    username: str
    email: str


int_pk = Annotated[int, mapped_column(primary_key=True)]
create_time = Annotated[str, mapped_column(default=datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))]


#  декларативный способ определения модели таблицы в БД
class UsersTable(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    username: Mapped[str]
    email: Mapped[str]
    create_time: Mapped[create_time]


#  императивный способ определения модели таблицы в БД
users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("email", String, unique=True)
)


class PersonalData(Base):
    __tablename__ = 'personal_data'

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    title: Mapped[str]
    create_time: Mapped[create_time]
