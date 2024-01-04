from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import CategoryService 
from app.models import User
from app.dto import CategoryDto
from app.database import get_db


def get_router(get_current_user) -> APIRouter:
    router = APIRouter(prefix="/expence", tags=["expence"])
    service = CategoryService()

    @router.post("/")
    def add(
        category_dto: CategoryDto,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        return service.add_expense(db=db, category_dto=category_dto, user_id=user.id)

    @router.get("/month/{category_id}")
    def get_mounth_expences(
        category_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        return service.show_current_mounth_expenses(
            db=db, category_id=category_id, user_id=user.id
        )

    @router.get("/all")
    def get_all(
        db: Session = Depends(get_db), user: User = Depends(get_current_user)
    ):
        return service.show_all_expenses(db=db,user_id=user.id)

    return router
