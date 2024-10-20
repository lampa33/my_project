from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(min_length=2, max_length=30)
    email: EmailStr | None
    full_name: str | None = Field(min_length=2, max_length=40)

class UserSchemaCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)

class UserSchemaFull(UserSchemaCreate):
    disabled: bool | None = False
