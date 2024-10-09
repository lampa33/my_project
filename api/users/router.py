from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth.utils import get_password_hash
from api.users.crud import create_user, get_current_user
from api.users.schemas import UserSchemaCreate, UserBase, UserSchemaFull
from core.models import db_helper

router = APIRouter(tags=['Users'])

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


@router.get("/users/me/", response_model=UserBase)
async def read_users_me(
    current_user: Annotated[UserSchemaFull, Depends(get_current_user)],
):
    return current_user
