from sqlalchemy import String, SmallInteger
from sqlalchemy.orm import Mapped, mapped_column

from timeline_app.database import db


class Category(db.Model):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(SmallInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    color: Mapped[str] = mapped_column(String(7), unique=False, nullable=False)
    icon_svg: Mapped[str] = mapped_column(String(64), nullable=False)
