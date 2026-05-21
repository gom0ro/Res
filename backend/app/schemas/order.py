from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.order import OrderStatus
from app.schemas.bar import Product as ProductSchema

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderItem(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price_at_time: float
    product: Optional[ProductSchema] = None

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    lounger_id: Optional[int] = None
    waiter_id: Optional[int] = None

class Order(BaseModel):
    id: int
    status: OrderStatus
    waiter_id: Optional[int] = None
    lounger_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    subtotal: float
    service_fee_percentage: float
    service_fee: float
    total_amount: float
    is_paid: bool
    items: List[OrderItem]

    class Config:
        from_attributes = True
