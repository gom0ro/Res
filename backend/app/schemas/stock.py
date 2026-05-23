from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StockReceiptCreate(BaseModel):
    product_id: int
    quantity: int
    cost_price: float
    sell_price: float
    note: Optional[str] = None

class StockReceiptOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    cost_price: float
    sell_price: float
    note: Optional[str] = None
    created_at: datetime
    product_name: Optional[str] = None

    class Config:
        from_attributes = True
