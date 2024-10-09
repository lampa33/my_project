from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None

class UserSchemaCreate(UserBase):
    password: str

class UserSchemaFull(UserBase):
    disabled: bool | None = False
    password: str