from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mssql.information_schema import constraints
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from .base import Base

class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    category_id: Mapped[int]=mapped_column(
        ForeignKey("productcategorys.id"),
    )

    category: Mapped["ProductCategory"] = relationship(back_populates="product")


class ProductCategory(Base):
    category: Mapped[str]

    product: Mapped[List["Product"]] = relationship(back_populates="category")