from typing import List, Optional

from sqlalchemy import String, SmallInteger, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from timeline_app.database import db


class Category(db.Model):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    color: Mapped[str] = mapped_column(String(7), unique=True, nullable=False)
    icon_svg: Mapped[str] = mapped_column(String(64), nullable=True)

    # icon_id: Mapped[int] = mapped_column(
    #     SmallInteger, ForeignKey("icon.id", ondelete="SET NULL"), unique=True, nullable=True
    # )
    # icon: Mapped[Optional["Icon"]] = relationship(back_populates="category")
    # events: Mapped[Optional[List["Category"]]] = relationship(back_populates="category")
