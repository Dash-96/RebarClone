from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    full_name: str | None = None
    hashed_password: str
    created_at: str | None = None
    updated_at: str | None = None
    is_active: bool | None = True
    role: str = "user"


class UserCreateDto(BaseModel):
    username: str
    password: str
    email: str
    role: str = 'user'
    full_name: str | None = None


class UserReadDto(BaseModel):
    id: int
    Username: str
    email: str
    full_name: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData():
    username: str
