from fastapi import FastAPI
from database_config import create_tables
from contextlib import asynccontextmanager
from routers import cart_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(cart_router.router)


@app.get('/')
async def read_root():
    return {'service': 'cart service'}
