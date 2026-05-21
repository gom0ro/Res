from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from datetime import datetime
import enum
from sqlalchemy import Enum

class PoolTariffType(str, enum.Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    CHILD = "child"
    VIP = "vip"

class PoolVisitStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    OVERDUE = "overdue"

class PoolVisit(Base):
    __tablename__ = "pool_visits"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=True)
    client_phone = Column(String, nullable=True)
    bracelet_number = Column(String, unique=True, index=True)
    tariff_type = Column(Enum(PoolTariffType), default=PoolTariffType.HOURLY)
    
    entry_time = Column(DateTime, default=datetime.utcnow)
    exit_time = Column(DateTime, nullable=True)
    expected_exit_time = Column(DateTime, nullable=True)
    
    status = Column(Enum(PoolVisitStatus), default=PoolVisitStatus.ACTIVE)
    total_amount = Column(Float, default=0.0)
    is_paid = Column(Boolean, default=False)
