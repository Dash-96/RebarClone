from fastapi import FastAPI
from routers import auth
from database_config import create_tables
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(auth.router)

if __name__ == "__main__":
    create_tables()

origins = ["http://127.0.0.1:8000", 'http://localhost:5173']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}
