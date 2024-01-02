from pydantic import BaseModel


class ExpenceDto(BaseModel):
    id: int | None = None
    sum: int

    def __str__(self):
        return f"{self.sum}"


class CategoryDto(BaseModel):
    id: int | None = None
    name: str | None = None
    expence: ExpenceDto | None = None

    def __str__(self):
        return f"{self.name}, {self.expence}"
