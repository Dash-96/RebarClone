import base64
from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile, status, Path
from databse_config import get_session
from sqlmodel import select, Session
from models.product_models import Product, ProductCreateDto, ProductResponseDto
from fastapi.security import OAuth2PasswordBearer

from typing import Annotated, List

router = APIRouter(
    prefix='/products',
    tags=['product']
)

session_dep = Annotated[Session, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='http://127.0.0.1:8001/auth/token')


async def extract_data(product_name: str = Form(), category_name: str = Form(), product_ingredients: str = Form(), base_price: int = Form()):
    return {'product_name': product_name, 'category_name': category_name, 'product_ingredients': product_ingredients, 'base_price': base_price}


@router.get('/get_all', response_model=List[ProductResponseDto])
async def read_all_products(session: session_dep):

    products: List[Product] = session.exec(select(Product)).all()
    products_response: List[ProductResponseDto] = []
    for product in products:
        products_response.append(ProductResponseDto(**product.model_dump()))
    return products_response


@router.get('/by_name/{product_name}', status_code=status.HTTP_202_ACCEPTED, response_model=ProductResponseDto)
async def read_by_name(session: session_dep, product_name: Annotated[str, Path()]):
    product = session.exec(select(Product).where(
        Product.product_name == product_name)).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Product with name {product_name} not found')
    product_response = ProductResponseDto(**product.model_dump())
    return product_response


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product(session: session_dep, image_file: UploadFile, product_data: Annotated[dict, Depends(extract_data)]):
    product = Product()
    for key, value in product_data.items():
        setattr(product, key, value)
    image_data = await image_file.read()
    product.image = base64.b64encode(image_data).decode('UTF-8')
    session.add(product)
    session.commit()


@router.delete('/delete_all')
async def delete_all(session: session_dep):
    products = session.exec(select(Product)).all()
    for product in products:
        session.delete(product)
    session.commit()


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, response_description='Product deleted')
async def delete_product_by_id(session: session_dep, product_id: Annotated[int, Path()]):
    product_to_delete = session.get(Product, product_id)
    if product_to_delete is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Product with id {product_id} not found')
    session.delete(product_to_delete)
    session.commit()


@router.put("/{product_id}")
async def update_product(session: session_dep, product_id: Annotated[int, Path()], updated_product: ProductCreateDto):
    product_to_update = session.get(Product, product_id)
    updated_product_dict = updated_product.model_dump()
    for key, value in updated_product_dict.items():
        setattr(product_to_update, key, value)
    session.add(product_to_update)
    session.commit()
