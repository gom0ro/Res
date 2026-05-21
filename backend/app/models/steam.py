from app.core.database import Base
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime
from datetime import datetime
import enum

class RoomType(str, enum.Enum):
    STEAM_ROOM = "steam_room"
    VIP_CABIN = "vip_cabin"

class RoomStatus(str, enum.Enum):
    FREE = "free"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    room_type = Column(Enum(RoomType))
    status = Column(Enum(RoomStatus), default=RoomStatus.FREE)
    price_per_hour = Column(Float, nullable=False)
    
    current_occupancy_start = Column(DateTime, nullable=True)
    current_occupancy_end = Column(DateTime, nullable=True)
