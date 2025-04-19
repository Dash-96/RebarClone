from typing import List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel


class Cart(SQLModel, table=True):
    __tablename__ = 'carts'
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None)
    coupoun: str | None = Field(default=None)
    cart_items: List["CartItem"] = Relationship(
        back_populates='cart', cascade_delete=True)


class CartCreate(SQLModel):
    user_id: int | None = Field(default=None)
    coupoun: str | None = Field(default=None)
    cart_items: List["CartItemCreate"] | None = Field(default=None)


class CartResponse(SQLModel):
    id: int | None
    user_id: int | None
    cart_items: List['CartItemCreate'] | None = None


class CartItem(SQLModel, table=True):
    __tablename__ = 'cart_items'
    id: int | None = Field(default=None, primary_key=True)
    price: float
    prodcut_name: str
    product_quantity: int
    cart_id: int = Field(foreign_key="carts.id", ondelete='CASCADE')
    cart: Cart | None = Relationship(back_populates='cart_items')


class CartItemCreate(SQLModel):
    price: float
    prodcut_name: str
    product_quantity: int
