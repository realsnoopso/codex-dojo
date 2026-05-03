"""API route aggregation."""

from fastapi import APIRouter

from src.routes.auth import router as auth_router
from src.routes.items import router as items_router
from src.routes.root import router as root_router

router: APIRouter = APIRouter()
router.include_router(root_router)
router.include_router(auth_router)
router.include_router(items_router)
