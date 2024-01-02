from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, MappedColumn
from app.database import Base
import datetime


class Category(Base):
    __tablename__ = "Category"

    id: Mapped[int] = MappedColumn(primary_key=True, unique=True)
    name: Mapped[str]

    expences: Mapped[list["Expence"]] = relationship(back_populates="category")


class Expence(Base):
    __tablename__ = "Expenses"

    id: Mapped[int] = MappedColumn(primary_key=True, unique=True)
    sum: Mapped[int]
    date: Mapped[datetime.datetime] = MappedColumn(default=datetime.datetime.now)
    category_id: Mapped[int] = MappedColumn(ForeignKey("Category.id"))

    category: Mapped["Category"] = relationship(back_populates="expences")
