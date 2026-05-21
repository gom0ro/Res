from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, date, time
from app.core.database import get_db
from app.models.finance import Transaction
from app.schemas.finance import Transaction as TransactionSchema

router = APIRouter()

@router.get("/", response_model=List[TransactionSchema])
async def get_transactions(
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    cashier_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(Transaction)
    
    if category:
        query = query.filter(Transaction.category == category)
    if cashier_id:
        query = query.filter(Transaction.cashier_id == cashier_id)
    if start_date:
        start_datetime = datetime.combine(start_date, time.min)
        query = query.filter(Transaction.created_at >= start_datetime)
    if end_date:
        end_datetime = datetime.combine(end_date, time.max)
        query = query.filter(Transaction.created_at <= end_datetime)
        
    query = query.order_by(Transaction.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/stats")
async def get_finance_stats(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    # Base filters
    filters = []
    if start_date:
        start_datetime = datetime.combine(start_date, time.min)
        filters.append(Transaction.created_at >= start_datetime)
    if end_date:
        end_datetime = datetime.combine(end_date, time.max)
        filters.append(Transaction.created_at <= end_datetime)

    # 1. Totals query
    totals_query = select(
        func.sum(Transaction.subtotal).label("total_subtotal"),
        func.sum(Transaction.service_fee).label("total_service_fee"),
        func.sum(Transaction.total_amount).label("total_amount"),
        func.count(Transaction.id).label("transaction_count")
    )
    for f in filters:
        totals_query = totals_query.filter(f)
        
    totals_res = await db.execute(totals_query)
    totals = totals_res.fetchone()
    
    # 2. Breakdown by category query
    breakdown_query = select(
        Transaction.category,
        func.sum(Transaction.total_amount).label("category_amount"),
        func.count(Transaction.id).label("category_count")
    )
    for f in filters:
        breakdown_query = breakdown_query.filter(f)
    breakdown_query = breakdown_query.group_by(Transaction.category)
    
    breakdown_res = await db.execute(breakdown_query)
    breakdown = breakdown_res.fetchall()
    
    category_data = {}
    for row in breakdown:
        category_data[row.category] = {
            "amount": row.category_amount or 0.0,
            "count": row.category_count or 0
        }

    return {
        "subtotal": totals.total_subtotal or 0.0,
        "service_fee": totals.total_service_fee or 0.0,
        "total": totals.total_amount or 0.0,
        "count": totals.transaction_count or 0,
        "breakdown": category_data
    }
