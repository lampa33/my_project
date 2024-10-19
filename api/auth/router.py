from datetime import timedelta
from os import access
from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth.crud import create_user
from api.users.schemas import UserSchemaCreate, UserBase, UserSchemaFull
from api.auth.schemas import oauth2_scheme
from api.auth.auth_exceptions import token_exception
from api.auth.utils import authenticate_user, get_current_user, get_password_hash, create_token, \
    TokenType, decode_token
from core.models import db_helper

router = APIRouter(tags=['Auth'])


@router.post("/login")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        response: Response,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await authenticate_user(
        session=session,
        username=form_data.username,
        password=form_data.password)
    payload_for_token = {"sub": user.username, "email": user.email, 'full_name': user.full_name}
    access_token = create_token(
        data=payload_for_token,
        token_type=TokenType.access,
    )
    refresh_token = create_token(
        data=payload_for_token,
        token_type=TokenType.refresh,
    )
    response.set_cookie(key='refresh_token', value=refresh_token)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/refresh")
async def renew_access_token(
        token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_token(token)
    if payload.pop(TokenType.token_type_key.value) != TokenType.refresh.value:
        raise token_exception
    access_token = create_token(
        data=payload,
        token_type=TokenType.access
    )
    return {"access_token": access_token}


@router.get("/users/me/", response_model=UserBase)
async def read_users_me(
    current_user: Annotated[UserSchemaFull, Depends(get_current_user)],
):
    return current_user


@router.post('/registration/')
async def create_new_user(
        user: UserSchemaCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user_dict = user.model_dump()
    password = user_dict.pop('password')
    hashed_password = get_password_hash(password)
    user_dict['hashed_password'] = hashed_password
    return await create_user(session, user_dict)