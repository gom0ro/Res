from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.steam import RoomType, RoomStatus

class RoomBase(BaseModel):
    name: str
    room_type: RoomType
    price_per_hour: float

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int
    status: RoomStatus
    current_occupancy_start: Optional[datetime] = None
    current_occupancy_end: Optional[datetime] = None
    reservation_time: Optional[str] = None

    class Config:
        from_attributes = True
