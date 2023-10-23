from typing import Optional, List

from sqlalchemy import String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from timeline_app.database import db


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    nick: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    # events: Mapped[Optional[List["Event"]]] = relationship(back_populates="user")

