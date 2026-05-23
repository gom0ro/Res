from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from datetime import datetime
import math
from app.core.database import get_db
from app.models.steam import Room, RoomType, RoomStatus
from app.schemas.steam import Room as RoomSchema, RoomCreate

router = APIRouter()

@router.get("/", response_model=List[RoomSchema])
async def get_rooms(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Room).order_by(Room.name))
    return result.scalars().all()

@router.post("/", response_model=RoomSchema)
async def create_room(room_in: RoomCreate, db: AsyncSession = Depends(get_db)):
    exist = await db.execute(select(Room).filter(Room.name == room_in.name))
    if exist.scalars().first():
        raise HTTPException(status_code=400, detail="Зал с таким названием уже существует")
    room = Room(
        name=room_in.name,
        room_type=room_in.room_type,
        price_per_hour=room_in.price_per_hour,
        status=RoomStatus.FREE
    )
    db.add(room)
    await db.commit()
    await db.refresh(room)
    return room

@router.delete("/{room_id}")
async def delete_room(room_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Room).filter(Room.id == room_id))
    room = result.scalars().first()
    if not room:
        raise HTTPException(status_code=404, detail="Зал не найден")
    if room.status == RoomStatus.OCCUPIED:
        raise HTTPException(status_code=400, detail="Нельзя удалить занятый зал")
    await db.delete(room)
    await db.commit()
    return {"msg": "Зал удалён"}

@router.post("/seed")
async def seed_rooms(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Room).limit(1))
    if result.scalars().first() is not None:
        return {"msg": "Already seeded"}
    db.add(Room(name="Хамам Лакшери", room_type=RoomType.STEAM_ROOM, price_per_hour=5000, status=RoomStatus.FREE))
    db.add(Room(name="Финская Сауна", room_type=RoomType.STEAM_ROOM, price_per_hour=4000, status=RoomStatus.FREE))
    db.add(Room(name="VIP Кабина №1", room_type=RoomType.VIP_CABIN, price_per_hour=10000, status=RoomStatus.FREE))
    db.add(Room(name="VIP Кабина №2", room_type=RoomType.VIP_CABIN, price_per_hour=10000, status=RoomStatus.FREE))
    db.add(Room(name="Русская Баня на дровах", room_type=RoomType.STEAM_ROOM, price_per_hour=6000, status=RoomStatus.FREE))
    await db.commit()
    return {"msg": "Seeded 5 spa/vip rooms"}

@router.post("/{room_id}/occupy", response_model=RoomSchema)
async def occupy_room(room_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Room).filter(Room.id == room_id))
    room = result.scalars().first()
    if not room:
        raise HTTPException(status_code=404, detail="Кабина/зал не найден")
    if room.status != RoomStatus.FREE:
        raise HTTPException(status_code=400, detail="Зал уже занят или находится на обслуживании")
    room.status = RoomStatus.OCCUPIED
    room.current_occupancy_start = datetime.utcnow()
    room.current_occupancy_end = None
    db.add(room)
    await db.commit()
    await db.refresh(room)
    return room

@router.post("/{room_id}/checkout")
async def checkout_room(
    room_id: int,
    payment_method: Optional[str] = "cash",
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Room).filter(Room.id == room_id))
    room = result.scalars().first()
    if not room:
        raise HTTPException(status_code=404, detail="Кабина/зал не найден")
    if room.status != RoomStatus.OCCUPIED or not room.current_occupancy_start:
        raise HTTPException(status_code=400, detail="Зал не был занят")

    now = datetime.utcnow()
    start_time = room.current_occupancy_start
    seconds = (now - start_time).total_seconds()
    hours = math.ceil(seconds / 3600.0)
    if hours < 1:
        hours = 1
    total_amount = hours * room.price_per_hour

    room.status = RoomStatus.FREE
    room.current_occupancy_start = None
    room.current_occupancy_end = None
    db.add(room)

    payment_label = "Каспий" if payment_method == "kaspi" else "Нал"
    from app.models.finance import Transaction
    txn = Transaction(
        category="room",
        item_name=f"Зона: {room.name} ({hours} ч.) [{payment_label}]",
        subtotal=total_amount,
        service_fee=0.0,
        total_amount=total_amount
    )
    db.add(txn)
    await db.commit()

    return {
        "status": "ok",
        "room_name": room.name,
        "price_per_hour": room.price_per_hour,
        "hours_billed": hours,
        "total_amount": total_amount,
        "start_time": start_time.isoformat(),
        "end_time": now.isoformat()
    }

@router.post("/{room_id}/status")
async def update_room_status(room_id: int, status: RoomStatus, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Room).filter(Room.id == room_id))
    room = result.scalars().first()
    if not room:
        raise HTTPException(status_code=404, detail="Кабина/зал не найден")
    room.status = status
    if status != RoomStatus.OCCUPIED:
        room.current_occupancy_start = None
        room.current_occupancy_end = None
    db.add(room)
    await db.commit()
    return {"status": "ok"}

@router.get("/", response_model=List[RoomSchema])
async def get_rooms(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Room).order_by(Room.name))
    return result.scalars().all()

@router.post("/seed")
async def seed_rooms(db: AsyncSession = Depends(get_db)):
    # Check if rooms exist with a fast limit check
    result = await db.execute(select(Room).limit(1))
    if result.scalars().first() is not None:
        return {"msg": "Already seeded"}

    # Add default rooms
    db.add(Room(name="Хамам Лакшери", room_type=RoomType.STEAM_ROOM, price_per_hour=5000, status=RoomStatus.FREE))
    db.add(Room(name="Финская Сауна", room_type=RoomType.STEAM_ROOM, price_per_hour=4000, status=RoomStatus.FREE))
    db.add(Room(name="VIP Кабина №1", room_type=RoomType.VIP_CABIN, price_per_hour=10000, status=RoomStatus.FREE))
    db.add(Room(name="VIP Кабина №2", room_type=RoomType.VIP_CABIN, price_per_hour=10000, status=RoomStatus.FREE))
    db.add(Room(name="Русская Баня на дровах", room_type=RoomType.STEAM_ROOM, price_per_hour=6000, status=RoomStatus.FREE))
    
    await db.commit()
    return {"msg": "Seeded 5 spa/vip rooms"}

@router.post("/{room_id}/occupy", response_model=RoomSchema)
async def occupy_room(room_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Room).filter(Room.id == room_id))
    room = result.scalars().first()
    if not room:
        raise HTTPException(status_code=404, detail="Кабина/зал не найден")
    
    if room.status != RoomStatus.FREE:
        raise HTTPException(status_code=400, detail="Зал уже занят или находится на обслуживании")
    
    room.status = RoomStatus.OCCUPIED
    room.current_occupancy_start = datetime.utcnow()
    room.current_occupancy_end = None
    
    db.add(room)
    await db.commit()
    await db.refresh(room)
    return room

@router.post("/{room_id}/checkout")
async def checkout_room(room_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Room).filter(Room.id == room_id))
    room = result.scalars().first()
    if not room:
        raise HTTPException(status_code=404, detail="Кабина/зал не найден")
    
    if room.status != RoomStatus.OCCUPIED or not room.current_occupancy_start:
        raise HTTPException(status_code=400, detail="Зал не был занят")

    now = datetime.utcnow()
    room.current_occupancy_end = now
    
    # Calculate duration
    start_time = room.current_occupancy_start
    duration = now - start_time
    seconds = duration.total_seconds()
    
    # Minimum of 1 hour, rounding up the hours
    hours = math.ceil(seconds / 3600.0)
    if hours < 1:
        hours = 1
        
    total_amount = hours * room.price_per_hour

    # Reset room
    room.status = RoomStatus.FREE
    room.current_occupancy_start = None
    room.current_occupancy_end = None
    
    db.add(room)

    # Register transaction
    from app.models.finance import Transaction
    txn = Transaction(
        category="room",
        item_name=f"Зона: {room.name} ({hours} ч.)",
        subtotal=total_amount,
        service_fee=0.0,
        total_amount=total_amount
    )
    db.add(txn)
    
    await db.commit()
    
    return {
        "status": "ok",
        "room_name": room.name,
        "price_per_hour": room.price_per_hour,
        "hours_billed": hours,
        "total_amount": total_amount,
        "start_time": start_time.isoformat(),
        "end_time": now.isoformat()
    }

@router.post("/{room_id}/status")
async def update_room_status(room_id: int, status: RoomStatus, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Room).filter(Room.id == room_id))
    room = result.scalars().first()
    if not room:
        raise HTTPException(status_code=404, detail="Кабина/зал не найден")
    
    room.status = status
    if status != RoomStatus.OCCUPIED:
        room.current_occupancy_start = None
        room.current_occupancy_end = None
        
    db.add(room)
    await db.commit()
    return {"status": "ok"}
