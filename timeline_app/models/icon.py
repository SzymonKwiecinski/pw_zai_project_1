from typing import List

from sqlalchemy import String, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from timeline_app.database import db


class Icon(db.Model):
    __tablename__ = "icon"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    value: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped["Category"] = relationship(back_populates="icon", cascade="all, delete, delete-orphan")
