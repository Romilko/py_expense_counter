from fastapi import Depends, FastAPI
from app.dto import CategoryDto
from app.services import CategoryService
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def hello_world():
    return {"Message":"Hello from expence counter"}


@app.get("/category")
def hello_world(db: Session = Depends(get_db)):
    return CategoryService.find_all(db)


@app.get("/category/{id}")
def get_category(id, db: Session = Depends(get_db)):
    return CategoryService.find_by_id(db, id)


@app.put("/category")
def add_category(category_dto: CategoryDto, db: Session = Depends(get_db)):
    category = CategoryService.add(db, category_dto)
    return category


@app.patch("/category")
def update_category(category_dto: CategoryDto, db: Session = Depends(get_db)):
    return CategoryService.update(db, category_dto)


@app.delete("/category/{id}")
def delete_category(id, db: Session = Depends(get_db)):
    try:
        id = int(id)
        return CategoryService.remove(db, id)
    except:
        return "Ошибка"


@app.patch("/add_expence")
def add_expence(category_dto: CategoryDto, db: Session = Depends(get_db)):
    return CategoryService.add_expence(db, category_dto)


@app.get("/show_expence/{id}")
def show_current_mounth_expences(id, db: Session = Depends(get_db)):
    return CategoryService.show_current_mounth_expences(db, id)
