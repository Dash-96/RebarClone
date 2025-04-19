from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class Product(SQLModel, table=True):
    __tablename__ = 'products'
    id: int | None = Field(default=None, primary_key=True)
    product_name: str = "relax"
    category_name: str = "Classic"
    product_ingredients: str = "something"
    base_price: int = 22
    image: str = "Blank"


class ProductCreateDto(BaseModel):
    product_name: str
    category_name: str
    product_ingredients: str | None = "mango, pineapple, passion fruit, apple juice, yogurt"
    base_price: int
    image: str | None = None


class ProductResponseDto(ProductCreateDto):
    pass
