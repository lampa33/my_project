from datetime import datetime, timezone, timedelta
from enum import Enum

import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.auth_exceptions import credentials_exception, auth_exception
from api.users.crud import get_user_by_username
from core.models import User
from core.config import settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class TokenType(Enum):
    token_type_key= 'token_type'
    access='access'
    refresh='refresh'

def decode_token(token: str):
    try:
        payload = jwt.decode(token, settings.public_key, algorithms=[settings.algorithm])
    except InvalidTokenError:
        raise credentials_exception
    return payload

def create_token(data: dict, token_type: TokenType):
    to_encode = data.copy()
    if token_type==token_type.refresh:
        expires_delta = timedelta(days=settings.refresh_token_expire_days)
    else:
        expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode[TokenType.token_type_key.value] = token_type.value
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.private_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_and_get_user(session: AsyncSession, username: str, password: str) -> User:
    user = await get_user_by_username(session=session, username=username)
    if not user or not verify_password(password, user.hashed_password):
        raise auth_exception
    return user


def get_password_hash(password):
    return pwd_context.hash(password)

