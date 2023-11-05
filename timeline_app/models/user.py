from sqlalchemy import String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from timeline_app.database import db


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
