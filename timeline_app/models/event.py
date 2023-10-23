from typing import Optional

from sqlalchemy import String, SmallInteger, Integer, Text, Date, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from timeline_app.database import db


class Event(db.Model):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    graphic: Mapped[str] = mapped_column(String(64), nullable=True)
    start_date: Mapped[str] = mapped_column(Date, nullable=False)
    end_date: Mapped[str] = mapped_column(Date, nullable=False)
    # user_id: Mapped[str] = mapped_column(SmallInteger, ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    category_id: Mapped[str] = mapped_column(SmallInteger, ForeignKey("category.id", ondelete="SET NULL"), nullable=True)
    # user: Mapped[Optional["User"]] = relationship(back_populates="events")
    category: Mapped[Optional["Category"]] = relationship(back_populates="events")
    CheckConstraint("end_date >= start_date", name="check_date")