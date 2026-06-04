from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StockReceiptCreate(BaseModel):
    product_id: int
    quantity: float
    cost_price: float
    sell_price: float
    note: Optional[str] = None

class StockReceiptOut(BaseModel):
    id: int
    product_id: int
    quantity: float
    cost_price: float
    sell_price: float
    note: Optional[str] = None
    created_at: datetime
    product_name: Optional[str] = None
    product_unit: Optional[str] = None

    class Config:
        from_attributes = True

class StockItemCreate(BaseModel):
    name: str
    unit: str = "кг"
    price: float = 0.0
