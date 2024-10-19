from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.users.schemas import UserSchemaFull
from core.models import User




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

