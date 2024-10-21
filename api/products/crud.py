from unicodedata import category

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.products.schemas import ProductCreate, CategorySchema
from core.models import Product,ProductCategory


async def get_all_products(session: AsyncSession):
    stmt = (select(
        Product.name, Product.description, Product.price, ProductCategory.category).join(
        ProductCategory, Product.category_id==ProductCategory.id)
    )
    products: Result
    products = await session.execute(stmt)
    return [product for product in products.mappings().all()]

async def get_product(session: AsyncSession, product_id) -> Product | None:
    return await session.get(Product, product_id)

async def create_product(session: AsyncSession, product_in: ProductCreate):
    product_dict = product_in.model_dump()
    prod_category = product_dict.pop('category')
    stmt = (select(
        ProductCategory.id).where(ProductCategory.category==prod_category)
    )
    result = await session.execute(stmt)
    category_id = result.scalars().first()

    product_dict['category_id']=category_id
    product = Product(**product_dict)
    session.add(product)
    await session.commit()
    return product

async def create_category(session: AsyncSession, category_in: CategorySchema) -> ProductCategory:
    category_of_product = ProductCategory(**category_in.model_dump())
    session.add(category_of_product)
    await session.commit()
    return category_of_product
