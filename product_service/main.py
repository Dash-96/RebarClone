from fastapi import FastAPI
from databse_config import create_tabels
from routers import product_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["http://127.0.0.1:8001", 'http://localhost:5173',
           'https://wr407hvl-5173.euw.devtunnels.ms']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router.router)

if __name__ == "__main__":
    create_tabels()


@app.get('/')
async def read_root():
    return {'page': 'Products'}
