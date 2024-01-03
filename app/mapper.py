from app.models import Category, Expense
from app.dto import CategoryDto, ExpenseDto


class CategoryMapper:
    def to_dto(category: Category):
        category_dto = CategoryDto()
        category_dto.id = category.id
        category_dto.name = category.name
        return category_dto

    def to_entity(category_dto: CategoryDto, user_id:int):
        category = Category()
        if category_dto.id != None:
            category.id = category_dto.id
        category.name = category_dto.name
        category.user_id = user_id
        return category


class ExpenseMapper:
    def to_dto(expence: Expense):
        expense_dto = ExpenseDto()
        expense_dto.id = expence.id
        expense_dto.sum = expence.sum
        return expense_dto

    def to_entity(expense_dto: ExpenseDto):
        expense = Expense()
        if expense_dto.id != None:
            expense.id = expense_dto.id
        expense.sum = expense_dto.sum
        return expense
