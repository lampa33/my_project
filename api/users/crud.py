from typing import Annotated

import jwt
from fastapi import Depends
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.auth.auth_exceptions import credentials_exception, disabled_user_exception
from api.auth.schemas import oauth2_scheme
from core.config import SECRET_KEY, ALGORITHM
from core.models import User, db_helper
from api.users.schemas import UserSchemaFull


async def create_user(session: AsyncSession, user_dict: dict) -> User:
    user = User(**user_dict)
    session.add(user)
    await session.commit()
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> UserSchemaFull | None:
    stmt = select(User).where(User.username == username)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        return
    return UserSchemaFull(
        username=user.username,
        password=user.hashed_password,
        email=user.email,
        full_name=user.full_name,
        disabled=user.disabled,
    )


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user = await get_user_by_username(session=session, username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(user: UserSchemaFull = Depends(get_current_user)):
    if not user.disabled:
        raise disabled_user_exception
    return user
