from fastapi import Depends, FastAPI
import fastapi_users
from app.dto import CategoryDto
from app.services import CategoryService
from sqlalchemy.orm import Session
from app.database import SessionLocal, Base, engine
from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead


Base.metadata.create_all(bind=engine)

app = FastAPI()


fastapi_users = fastapi_users.FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(          #авторизация
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(        #регистрация
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

get_current_user = fastapi_users.current_user()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def hello_world():
    return {"Message":"Hello world"}

@app.get("/category")
def hello_world(db: Session = Depends(get_db), user:User = Depends(get_current_user)):
    return CategoryService.find_all(db=db,user_id=user.id)


@app.get("/category/{category_id}")
def get_category(category_id:int, db: Session = Depends(get_db),user:User = Depends(get_current_user)):
    return CategoryService.find_by_id(db=db, category_id = category_id, user_id = user.id)


@app.post("/category")
def add_category(category_dto: CategoryDto, db: Session = Depends(get_db),user:User = Depends(get_current_user)):
    category = CategoryService.add(db=db, category_dto=category_dto, user_id = user.id)
    return category


@app.patch("/category")
def update_category(category_dto: CategoryDto, db: Session = Depends(get_db),user:User = Depends(get_current_user)):
    return CategoryService.update(db=db, category_dto = category_dto, user_id=user.id)


@app.delete("/category/{category_id}")
def delete_category(category_id:int, db: Session = Depends(get_db),user:User = Depends(get_current_user)):
    try:
        category_id = int(category_id)
        return CategoryService.remove(db=db, category_id=category_id,user_id=user.id)
    except:
        return "Ошибка"


@app.post("/add_expense")
def add_expence(category_dto: CategoryDto, db: Session = Depends(get_db),user:User = Depends(get_current_user)):
    return CategoryService.add_expense(db = db, category_dto = category_dto, user_id = user.id)


@app.get("/show_expense/{category_id}")
def show_current_mounth_expences(category_id:int, db: Session = Depends(get_db),user:User = Depends(get_current_user)):
    return CategoryService.show_current_mounth_expenses(db=db, category_id=category_id,user_id = user.id)

@app.get("/show_expense")
def show_all_expense(db: Session = Depends(get_db),user:User = Depends(get_current_user)):
    return CategoryService.show_all_expenses(db=db, user_id=user.id)