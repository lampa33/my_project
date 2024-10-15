from datetime import datetime, timezone, timedelta
from typing import Annotated

import jwt
from fastapi import Depends
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.crud import get_user_by_username
from api.auth.schemas import oauth2_scheme, UserSchema
from api.auth.users_exceptions import credentials_exception, disabled_user_exception, auth_exception
from core.models import db_helper
from core.config import settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user_by_username(session=session, username=username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(user: UserSchema = Depends(get_current_user)):
    if not user.disabled:
        raise disabled_user_exception
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(session: AsyncSession, username: str, password: str):
    user = await get_user_by_username(session=session, username=username)
    if not user or not verify_password(password, user.password):
        raise auth_exception
    return user


def get_password_hash(password):
    return pwd_context.hash(password)

