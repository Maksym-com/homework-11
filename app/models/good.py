from __future__ import annotations
from datetime import date

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Good(Base):
    __tablename__ = "good"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(Text())

    def __repr__(self):
        return f"Post: {self.name}"

    def __str__(self):
        return self.name.capitalize()

