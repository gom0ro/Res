from pydantic import BaseModel
from typing import Optional
from app.models.lounger import LoungerStatus

class LoungerBase(BaseModel):
    number: str
    zone: str
    price_per_hour: float

class LoungerCreate(LoungerBase):
    pass

class Lounger(LoungerBase):
    id: int
    status: LoungerStatus
    current_booking_id: Optional[int] = None

    class Config:
        from_attributes = True
