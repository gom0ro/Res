from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.pool import PoolTariffType, PoolVisitStatus

class PoolVisitBase(BaseModel):
    client_name: Optional[str] = None
    client_phone: Optional[str] = None
    bracelet_number: str
    tariff_type: PoolTariffType

class PoolVisitCreate(PoolVisitBase):
    expected_hours: int = 2

class PoolVisit(PoolVisitBase):
    id: int
    entry_time: datetime
    exit_time: Optional[datetime] = None
    expected_exit_time: Optional[datetime] = None
    status: PoolVisitStatus
    total_amount: float
    is_paid: bool

    class Config:
        from_attributes = True
