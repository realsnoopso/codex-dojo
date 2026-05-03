from fastapi import APIRouter

from src.routes.items import router as items_router


router: APIRouter = APIRouter()
router.include_router(items_router)

