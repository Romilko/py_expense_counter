import datetime
from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.models import Category, Expense
from app.dto import CategoryDto
from app.mapper import CategoryMapper, ExpenseMapper


class CategoryService:

    def find_all(self, db: Session, user_id: int):
        return db.query(Category).filter(Category.user_id == user_id).all()

    def find_by_id(self, db: Session, category_id: int, user_id: int):
        return (
            db.query(Category)
            .filter(Category.id == category_id, Category.user_id == user_id)
            .one_or_none()
        )

    def add(self, db: Session, category_dto: CategoryDto, user_id: int):
        category = CategoryMapper.to_entity(category_dto, user_id)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def remove(self, db: Session, category_id: int, user_id: int):
        category = (
            db.query(Category)
            .filter(Category.id == category_id, Category.user_id == user_id)
            .one_or_none()
        )
        db.delete(category)
        db.commit()
        return f"Категория {category.name} удалена."

    def update(self, db: Session, category_dto: CategoryDto, user_id: int):
        category_id = category_dto.id
        category = (
            db.query(Category)
            .filter(Category.id == category_id, Category.user_id == user_id)
            .one_or_none()
        )
        category.name = category_dto.name
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def add_expense(self, db: Session, category_dto: CategoryDto, user_id: int):
        category_id = category_dto.id
        category = (
            db.query(Category)
            .filter(Category.id == category_id, Category.user_id == user_id)
            .one_or_none()
        )
        expense = ExpenseMapper.to_entity(category_dto.expense)
        expense.user_id = user_id
        category.expenses.append(expense)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def show_current_mounth_expenses(self, db: Session, category_id: int, user_id: int):
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        # category = db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).one_or_none()
        # expenses = list(filter((lambda x: x.date.month==month and x.date.year==year),category.expenses))
        expenses = (
            db.query(Expense)
            .filter(
                (extract("year", Expense.date) == year),
                extract("month", Expense.date) == month,
                Expense.category_id == category_id,
                Expense.user_id == user_id,
            )
            .all()
        )
        my_map = {}
        my_map["Amount of expenses"] = sum(list(map(lambda x: x.sum, expenses)))
        my_map["Expenses"] = expenses
        return my_map

    def show_all_expenses(self,db: Session, user_id: int):
        expenses = db.query(Expense).filter(Expense.user_id == user_id).all()
        my_map = {}
        my_map["Amount of expenses"] = sum(list(map(lambda x: x.sum, expenses)))
        my_map["Expenses"] = expenses
        return my_map

    def test(self, db: Session):
        return db.query(Category).all()
