from sqlalchemy import (
    String,
    SmallInteger,
    Integer,
    Text,
    Date,
    ForeignKey,
    CheckConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from timeline_app.database import db


class Event(db.Model):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    graphic: Mapped[str] = mapped_column(String(64), nullable=True)
    start_date: Mapped[str] = mapped_column(Date, nullable=False)
    end_date: Mapped[str] = mapped_column(Date, nullable=False)
    category_id: Mapped[str] = mapped_column(
        SmallInteger, ForeignKey("category.id", ondelete="SET NULL"), nullable=True
    )
    CheckConstraint("end_date >= start_date", name="check_date")
