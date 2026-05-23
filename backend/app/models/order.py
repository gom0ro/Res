from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

class OrderStatus(str, enum.Enum):
    NEW = "new"
    PREPARING = "preparing"
    READY = "ready"
    SERVED = "served"
    COMPLETED = "completed"   # доставлен официантом
    PAID = "paid"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.NEW)
    
    waiter_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    lounger_id = Column(Integer, ForeignKey("loungers.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    subtotal = Column(Float, default=0.0)
    service_fee_percentage = Column(Float, default=10.0)
    service_fee = Column(Float, default=0.0)
    total_amount = Column(Float, default=0.0)
    
    is_paid = Column(Boolean, default=False)

    waiter = relationship("User", back_populates="orders", foreign_keys=[waiter_id])
    lounger = relationship("Lounger", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("bar_products.id"))
    
    quantity = Column(Integer, default=1)
    price_at_time = Column(Float) # Store the price at the time of order
    
    order = relationship("Order", back_populates="items")
    product = relationship("BarProduct")
