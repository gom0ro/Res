from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class LoungerStatus(str, enum.Enum):
    FREE = "free"
    OCCUPIED = "occupied"
    RESERVED = "reserved"
    MAINTENANCE = "maintenance"

class Lounger(Base):
    __tablename__ = "loungers"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, index=True)
    zone = Column(String, default="main") # e.g. VIP, main pool, kids
    status = Column(Enum(LoungerStatus), default=LoungerStatus.FREE)
    price_per_hour = Column(Float, default=0.0)
    
    current_booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=True)
    
    # Active orders associated with this lounger
    orders = relationship("Order", back_populates="lounger")


class BookingStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    lounger_id = Column(Integer, ForeignKey("loungers.id"))
    client_name = Column(String)
    client_phone = Column(String)
    
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(Enum(BookingStatus), default=BookingStatus.ACTIVE)
    
    total_amount = Column(Float, default=0.0)
