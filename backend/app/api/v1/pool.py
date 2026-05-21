from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.pool import PoolVisit, PoolVisitStatus
from app.schemas.pool import PoolVisit as PoolVisitSchema, PoolVisitCreate
from app.core.dependencies import get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[PoolVisitSchema])
async def get_pool_visits(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PoolVisit).order_by(PoolVisit.entry_time.desc()))
    return result.scalars().all()

@router.post("/", response_model=PoolVisitSchema)
async def create_pool_visit(visit_in: PoolVisitCreate, db: AsyncSession = Depends(get_db)):
    # Check if bracelet is already active
    result = await db.execute(select(PoolVisit).filter(
        PoolVisit.bracelet_number == visit_in.bracelet_number,
        PoolVisit.status == PoolVisitStatus.ACTIVE
    ))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Браслет уже используется")

    now = datetime.utcnow()
    expected_exit = now + timedelta(hours=visit_in.expected_hours) if visit_in.expected_hours else None

    # Calculate base price (mock logic)
    prices = {"hourly": 2000, "daily": 10000, "child": 1000, "vip": 5000}
    amount = prices.get(visit_in.tariff_type.value, 2000) * (visit_in.expected_hours or 1)

    visit = PoolVisit(
        client_name=visit_in.client_name,
        client_phone=visit_in.client_phone,
        bracelet_number=visit_in.bracelet_number,
        tariff_type=visit_in.tariff_type,
        entry_time=now,
        expected_exit_time=expected_exit,
        total_amount=amount,
        status=PoolVisitStatus.ACTIVE
    )
    
    db.add(visit)
    await db.commit()
    await db.refresh(visit)
    return visit

@router.post("/{visit_id}/checkout")
async def checkout_pool_visit(visit_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PoolVisit).filter(PoolVisit.id == visit_id))
    visit = result.scalars().first()
    
    if not visit:
        raise HTTPException(status_code=404, detail="Посещение не найдено")
    
    visit.status = PoolVisitStatus.COMPLETED
    visit.exit_time = datetime.utcnow()
    visit.is_paid = True
    
    # Register transaction
    from app.models.finance import Transaction
    txn = Transaction(
        category="pool",
        item_name=f"Бассейн: браслет #{visit.bracelet_number} ({visit.client_name or 'Гость'})",
        subtotal=visit.total_amount,
        service_fee=0.0,
        total_amount=visit.total_amount
    )
    db.add(txn)
    
    await db.commit()
    return {"status": "ok"}
