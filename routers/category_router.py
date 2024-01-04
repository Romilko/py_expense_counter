from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import CategoryService
from app.dto import CategoryDto
from app.models import User
from app.database import get_db


def get_router(get_current_user) -> APIRouter:
    service = CategoryService()

    router = APIRouter(prefix="/category", tags=["category"])

    @router.get("/")
    def get_all(
        db: Session = Depends(get_db), user: User = Depends(get_current_user)
    ):
        return service.find_all(db=db, user_id=user.id)

    @router.get("/{category_id}")
    def get_by_id(
        category_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        return service.find_by_id(db=db, category_id=category_id, user_id=user.id)

    @router.post("/")
    def add(
        category_dto: CategoryDto,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        category = service.add(db=db, category_dto=category_dto, user_id=user.id)
        return category

    @router.patch("/")
    def update(
        category_dto: CategoryDto,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        return service.update(db=db, category_dto=category_dto, user_id=user.id)

    @router.delete("/{category_id}")
    def delete(
        category_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
    ):
        return service.remove(db=db, category_id=category_id, user_id=user.id)

    return router
