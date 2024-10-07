from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth.crud import create_user
from api.auth.schemas import UserSchemaCreate, UserSchema, UserBase
from api.auth.utils import create_access_token, authenticate_user, get_current_user, get_password_hash
from core.models import db_helper

router = APIRouter(tags=['Auth'])

ACCESS_TOKEN_EXPIRE_MINUTES = 3

@router.post("/login")
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await authenticate_user(
        session=session,
        username=form_data.username,
        password=form_data.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "email": user.email, 'full_name': user.full_name},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



@router.get("/users/me/", response_model=UserBase)
async def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_user)],
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