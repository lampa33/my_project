from enum import Enum

from pydantic import BaseModel, ConfigDict
from sqlalchemy.sql.annotation import Annotated


class ProductCategory(Enum):
    clothing='clothing'
    shoes='shoes'
    accessories='accessories'
    sports='sports'

class ProductBase(BaseModel):
    name: str
    description: str
    price: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class CategorySchema(BaseModel):
    category: ProductCategory

