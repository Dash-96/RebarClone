from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from database_config import get_session
from models.cart_models import Cart, CartCreate, CartItem, CartResponse, CartItemCreate

router = APIRouter(
    prefix='/cart',
    tags=['cart']
)

session_dep = Annotated[Session, Depends(get_session)]


@router.get('/all_carts', response_model=list[CartResponse])
async def read_all(session: session_dep):
    carts = session.exec(select(Cart).options(
        selectinload(Cart.cart_items))).all()
    return carts


@router.post('/create')
async def create_cart(session: session_dep, cart_dto: CartCreate):
    cart_data = cart_dto.model_dump()
    cart_items = cart_data.pop('cart_items', [])
    cart = Cart(**cart_data)
    cart.cart_items = [CartItem(**item) for item in cart_items]
    session.add(cart)
    session.commit()


@router.post('/create_cart_item/{cart_id}')
async def create_cart_item(session: session_dep, cart_item_create: CartItemCreate, cart_id: Annotated[int, Path()]):
    cart_item = CartItem(**cart_item_create.model_dump(), cart_id=cart_id)
    session.add(cart_item)
    session.commit()
