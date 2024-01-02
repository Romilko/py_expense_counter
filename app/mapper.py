from app.models import Category, Expence
from app.dto import CategoryDto, ExpenceDto


class CategoryMapper:
    def to_dto(category: Category):
        category_dto = CategoryDto()
        category_dto.id = category.id
        category_dto.name = category.name
        return category_dto

    def to_entity(category_dto: CategoryDto):
        category = Category()
        if category_dto.id != None:
            category.id = category_dto.id
        category.name = category_dto.name
        return category


class ExpenceMapper:
    def to_dto(expence: Expence):
        expence_dto = ExpenceDto()
        expence_dto.id = expence.id
        expence_dto.sum = expence.sum
        return expence_dto

    def to_entity(expence_dto: ExpenceDto):
        expence = Expence()
        if expence_dto.id != None:
            expence.id = expence_dto.id
        expence.sum = expence_dto.sum
        return expence
