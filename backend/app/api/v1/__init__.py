from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.staff import router as staff_router
from app.api.v1.pool import router as pool_router
from app.api.v1.loungers import router as loungers_router
from app.api.v1.bar import router as bar_router
from app.api.v1.steam import router as steam_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.finance import router as finance_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(staff_router, prefix="/staff", tags=["staff"])
api_router.include_router(pool_router, prefix="/pool", tags=["pool"])
api_router.include_router(loungers_router, prefix="/loungers", tags=["loungers"])
api_router.include_router(bar_router, prefix="/bar", tags=["bar"])
api_router.include_router(steam_router, prefix="/steam", tags=["steam"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(finance_router, prefix="/finance", tags=["finance"])
