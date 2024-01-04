from pydantic import BaseModel


class ExpenseDto(BaseModel):
    id: int | None = None
    sum: int

    def __str__(self):
        return f"{self.sum}"


class CategoryDto(BaseModel):
    id: int | None = None
    name: str | None = None
    user_id: int | None = None
    expense: ExpenseDto | None = None

    def __str__(self):
        return f"{self.name}, {self.expence}"
