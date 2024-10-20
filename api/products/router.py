from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import db_helper
from . import crud
from .crud import create_category
from .dependencies import product_by_id
from .schemas import ProductCreate, Product, CategorySchema

router = APIRouter(tags=["Products"])

@router.get('/')
async def get_all_products(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await crud.get_all_products(session=session)


@router.post('/', response_model=Product)
async def create_product(
        product_in: ProductCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),):
    return await crud.create_product(session=session, product_in=product_in)


@router.get('/{product_id}/', response_model=Product)
async def get_product(
        product: Product = Depends(product_by_id)
):
    return product

@router.post('/category')
async def create_new_product_category(
        category: CategorySchema,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await create_category(session=session, category_in=category)
    return 'Added successfully'
