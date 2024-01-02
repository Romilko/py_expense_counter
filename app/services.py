import datetime
from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.models import Category, Expence
from app.dto import CategoryDto
from app.mapper import CategoryMapper, ExpenceMapper


class CategoryService:
    def find_all(db: Session):
        return db.query(Category).all()

    def find_by_id(db: Session, id: int):
        return db.query(Category).filter(Category.id == id).one()

    def add(db: Session, category_dto: CategoryDto):
        category = CategoryMapper.to_entity(category_dto)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def remove(db: Session, id):
        category = db.query(Category).filter(Category.id == id).one()
        db.delete(category)
        db.commit()
        return f"Категория {category.name} удалена."

    def update(db: Session, category_dto: CategoryDto):
        id = category_dto.id
        category = db.query(Category).filter(Category.id == id).one()
        category.name = category_dto.name
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def add_expence(db: Session, category_dto: CategoryDto):
        id = category_dto.id
        category = db.query(Category).filter(Category.id == id).one()
        expence = ExpenceMapper.to_entity(category_dto.expence)
        print(expence)
        category.expences.append(expence)
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def show_current_mounth_expences(db: Session, id):
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        expence = (
            db.query(Expence)
            .filter(
                (extract("year", Expence.date) == year),
                extract("month", Expence.date) == month,
                Expence.category_id == id,
            )
            .all()
        )
        my_map = {}
        my_map["Amount of expenses"] = sum(list(map(lambda x: x.sum, expence)))
        my_map["Expenses"] = expence
        return my_map
