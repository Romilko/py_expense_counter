from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, MappedColumn
from sqlalchemy import String, Boolean
from app.database import Base
import datetime


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    id: Mapped[int] = MappedColumn(primary_key=True, unique=True)
    name: Mapped[str]
    email: Mapped[str] = MappedColumn(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = MappedColumn(String(length=1024), nullable=False)
    is_active: Mapped[bool] = MappedColumn(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = MappedColumn(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = MappedColumn(Boolean, default=False, nullable=False)

    categoryes: Mapped[list["Category"]] = relationship(back_populates="user")
    expenses: Mapped[list["Expense"]] = relationship(back_populates="user")

class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = MappedColumn(primary_key=True, unique=True)
    name: Mapped[str]
    user_id: Mapped[int]=MappedColumn(ForeignKey("user.id"))

    user:Mapped["User"]= relationship(back_populates="categoryes")
    expenses: Mapped[list["Expense"]] = relationship(back_populates="category")

class Expense(Base):
    __tablename__ = "expense"

    id: Mapped[int] = MappedColumn(primary_key=True, unique=True)
    sum: Mapped[int]
    date: Mapped[datetime.datetime] = MappedColumn(default=datetime.datetime.now)

    user_id:Mapped[int] = MappedColumn(ForeignKey("user.id"))
    user:Mapped["User"] = relationship(back_populates="expenses")

    category_id: Mapped[int] = MappedColumn(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(back_populates="expenses")

