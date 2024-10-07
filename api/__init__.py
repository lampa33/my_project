from fastapi import APIRouter

from core.config import settings
from .products.router import router as products_router
from .auth.router import router as auth_router

router = APIRouter(prefix=settings.api_v1_prefix)

router.include_router(products_router, prefix='/products')
router.include_router(auth_router, prefix='/auth')