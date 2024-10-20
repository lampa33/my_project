
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.products.schemas import ProductCreate, CategorySchema
from core.models import Product
from core.models.product import ProductCategory


async def get_all_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result
    result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)

async def get_product(session: AsyncSession, product_id) -> Product | None:
    return await session.get(Product, product_id)

async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    return product

async def create_category(session: AsyncSession, category_in: CategorySchema) -> ProductCategory:
    category_of_product = ProductCategory(**category_in.model_dump())
    session.add(category_of_product)
    await session.commit()
    return category_of_product
