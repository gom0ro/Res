from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from datetime import datetime, date
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.pool import PoolVisit, PoolVisitStatus
from app.models.lounger import Lounger, LoungerStatus
from app.models.order import Order, OrderStatus
from app.models.user import User

router = APIRouter()

@router.get("/stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db), _user: User = Depends(get_current_active_user)):
    # 1. Active pool guests: fast SQL COUNT
    active_pool_res = await db.execute(
        select(func.count(PoolVisit.id)).filter(PoolVisit.status == PoolVisitStatus.ACTIVE)
    )
    active_pool_guests = active_pool_res.scalar() or 0

    # 2. Lounger occupancy rate: fast SQL COUNTs
    total_loungers_res = await db.execute(select(func.count(Lounger.id)))
    total_loungers = total_loungers_res.scalar() or 0

    occupied_loungers_res = await db.execute(
        select(func.count(Lounger.id)).filter(Lounger.status != LoungerStatus.FREE)
    )
    occupied_loungers = occupied_loungers_res.scalar() or 0
    
    occupancy_percentage = 0
    if total_loungers > 0:
        occupancy_percentage = round((occupied_loungers / total_loungers) * 100)

    # 3. Active bar orders: fast SQL COUNT
    active_orders_res = await db.execute(
        select(func.count(Order.id)).filter(
            Order.status != OrderStatus.PAID, 
            Order.status != OrderStatus.CANCELLED,
            Order.status != OrderStatus.COMPLETED
        )
    )
    active_orders_count = active_orders_res.scalar() or 0

    # 4. Daily revenue calculation: fast SQL SUMs
    today_start = datetime.combine(date.today(), datetime.min.time())
    
    pool_revenue_res = await db.execute(
        select(func.sum(PoolVisit.total_amount)).filter(
            PoolVisit.status == PoolVisitStatus.COMPLETED,
            PoolVisit.exit_time >= today_start
        )
    )
    pool_revenue = pool_revenue_res.scalar() or 0.0

    bar_revenue_res = await db.execute(
        select(func.sum(Order.total_amount)).filter(
            Order.created_at >= today_start
        )
    )
    bar_revenue = bar_revenue_res.scalar() or 0.0

    # Base operational mock revenue for luxury cabins + real aggregates
    total_revenue = pool_revenue + bar_revenue

    return {
        "daily_revenue": f"{total_revenue:,.0f} ₸".replace(",", " "),
        "active_pool_guests": active_pool_guests,
        "loungers_occupancy": f"{occupancy_percentage}%",
        "active_orders": active_orders_count
    }
