from enum import Enum

from pydantic import BaseModel, ConfigDict


class ProductCategory(str, Enum):
    clothing='clothing'
    shoes='shoes'
    accessories='accessories'
    sports='sports'

class ProductBase(BaseModel):
    name: str
    description: str
    price: int

class ProductCreate(ProductBase):
    category: ProductCategory

class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class CategorySchema(BaseModel):
    category: ProductCategory

