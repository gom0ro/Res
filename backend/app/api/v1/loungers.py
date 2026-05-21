from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.core.database import get_db
from app.models.lounger import Lounger, LoungerStatus
from app.schemas.lounger import Lounger as LoungerSchema, LoungerCreate

router = APIRouter()

@router.get("/", response_model=List[LoungerSchema])
async def get_loungers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lounger))
    return result.scalars().all()

@router.post("/seed")
async def seed_loungers(db: AsyncSession = Depends(get_db)):
    # Quick utility to seed loungers for testing
    count_res = await db.execute(select(Lounger))
    if len(count_res.scalars().all()) > 0:
        return {"msg": "Already seeded"}

    for i in range(1, 13):
        db.add(Lounger(number=f"T-{i}", zone="main", price_per_hour=3000))
    for i in range(1, 5):
        db.add(Lounger(number=f"V-{i}", zone="vip", price_per_hour=8000))
    
    await db.commit()
    return {"msg": "Seeded 16 loungers"}

@router.post("/{lounger_id}/status")
async def update_lounger_status(lounger_id: int, status: LoungerStatus, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lounger).filter(Lounger.id == lounger_id))
    lounger = result.scalars().first()
    if not lounger:
        raise HTTPException(status_code=404, detail="Топчан не найден")
    
    lounger.status = status
    await db.commit()
    return {"status": "ok"}
