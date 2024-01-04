from fastapi import Depends, FastAPI
import fastapi_users
from app.services import CategoryService
from sqlalchemy.orm import Session
from app.database import Base, engine
from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from routers import category_router, expense_router



Base.metadata.create_all(bind=engine)

app = FastAPI()


fastapi_users = fastapi_users.FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

get_current_user = fastapi_users.current_user()

app.include_router(  # авторизация
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(  # регистрация
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    category_router.get_router(get_current_user=get_current_user)
)

app.include_router(
    expense_router.get_router(get_current_user=get_current_user)
)


@app.get("/")
def hello_world():
    return {"Message": "Hello world"}
