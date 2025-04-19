from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from models.user_models import UserCreateDto, UserReadDto, User, Token, TokenData
from typing import Annotated
from database_config import get_session, Session
from sqlmodel import select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
import jwt

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

SECRET_KEY = 'b519ee8108021e5a6e6ea3435e646d5447a987aca0d7bbdf073e723bb1ae861b'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

session_dep = Annotated[Session, Depends(get_session)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

password_context = CryptContext(schemes=["bcrypt"])

# This function is used to create a hashed password using bcrypt algorithm.


def get_hash_password(password: str) -> str:
    return password_context.hash(password)

# This function is used to verify if the provided plain password matches the hashed password.


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

# This function is used to create a JWT access token with an expiration time.


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    token = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return token


def autenticate_user(session: Session, username: str, password: str):
    user = session.exec(select(User).where(User.username == username)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='User not found')
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect password')
    return user


def get_current_user(session: session_dep, token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        username = payload['sub']
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
        token_data = TokenData(username)
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    user = session.exec(select(User).where(
        User.username == token_data.username))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
    return user


@router.post('/user/signup', status_code=status.HTTP_201_CREATED)
async def create_user(user_created: UserCreateDto, session: session_dep) -> None:
    password = get_hash_password(user_created.password)
    user = User(**user_created.model_dump(), hashed_password=password)
    user.created_at = datetime.now()
    session.add(user)
    session.commit()


@router.post('/token')
async def login_for_access_token(session: session_dep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = autenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password')
    data = {'sub': user.username}
    token = create_access_token(data, timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return Token(access_token=token, token_type='bearer')


@router.get('/user')
async def read_current_user(user: Annotated[User, Depends(get_current_user)]):
    return user
