from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None

class UserSchemaCreate(UserBase):
    password: str

class UserSchema(UserBase):
    disabled: bool | None = False
    password: str


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")