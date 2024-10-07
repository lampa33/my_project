from sqlalchemy.orm import Mapped

from .base import Base

class User(Base):
    username: Mapped[str]
    email: Mapped[str]
    full_name: Mapped[str]
    hashed_password: Mapped[str]
    disabled: Mapped[bool] = False