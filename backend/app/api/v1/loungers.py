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

@router.post("/", response_model=LoungerSchema)
async def create_lounger(lounger_in: LoungerCreate, db: AsyncSession = Depends(get_db)):
    # Check if number already exists
    result = await db.execute(select(Lounger).filter(Lounger.number == lounger_in.number))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Топчан с таким номером уже существует")
    lounger = Lounger(
        number=lounger_in.number,
        zone=lounger_in.zone,
        price_per_hour=lounger_in.price_per_hour
    )
    db.add(lounger)
    await db.commit()
    await db.refresh(lounger)
    return lounger

@router.delete("/{lounger_id}")
async def delete_lounger(lounger_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lounger).filter(Lounger.id == lounger_id))
    lounger = result.scalars().first()
    if not lounger:
        raise HTTPException(status_code=404, detail="Топчан не найден")
    await db.delete(lounger)
    await db.commit()
    return {"msg": "Топчан удалён"}

@router.post("/seed")
async def seed_loungers(db: AsyncSession = Depends(get_db)):
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
