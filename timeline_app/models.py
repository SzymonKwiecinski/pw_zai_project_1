import datetime
from typing import List, Optional

from sqlmodel import create_engine, Field, SQLModel, Session, select, Relationship, ForeignKey
# https://github.com/tiangolo/sqlmodel/issues/213
# https://docs.sqlalchemy.org/en/20/orm/cascades.html#unitofwork-cascades
url = "postgresql://postgres:postgres@127.0.0.1:2022/timeline_app_db"
engine = create_engine(url, echo=True)


class Users(SQLModel, table=True):
    id: int = Field(primary_key=True, ge=-32768, le=32767)
    nick: str = Field(max_length=64)
    email: str = Field(max_length=64)
    password: str = Field(max_length=128)
    # events: List["Events"] = Relationship(sa_relationship_kwargs={"cascade": "all, delete"})


class Icons(SQLModel, table=True):
    id: int = Field(primary_key=True, ge=-32768, le=32767)
    email: str = Field(max_length=64)
    value: str


class Categories(SQLModel, table=True):
    id: int = Field(primary_key=True, ge=-32768, le=32767)
    name: str = Field(max_length=64)
    color: Optional[str] = Field(None, max_length=7)
    icon_id: int = Field(foreign_key="icons.id", ge=-32768, le=32767)


class Events(SQLModel, table=True):
    id: int = Field(primary_key=True, ge=-2147483648, le=2147483647)
    name: str = Field(max_length=64)
    description: Optional[str] = Field(None)
    graphic: Optional[str] = Field(None, max_length=64)
    start_date: datetime.date
    end_date: datetime.date
    user_id: Optional[int] = Field(None, foreign_key="users.id", ge=-32768, le=32767)
    category_id: Optional[int] = Field(None, foreign_key="categories.id", ge=-32768, le=32767)


def select_heroes():
    with Session(engine) as session:
        statement = select(Users).where(Users.id == 'szymon')
        res = session.exec(statement)
        for x in res:
            print(x)


