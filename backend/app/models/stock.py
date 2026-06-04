from app.core.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class StockItem(Base):
    __tablename__ = "stock_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    stock_quantity = Column(Float, default=0.0)
    unit = Column(String, default="кг")
    price = Column(Float, default=0.0)  # учётная цена за единицу
    is_active = Column(Boolean, default=True)

class StockReceipt(Base):
    __tablename__ = "stock_receipts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("stock_items.id"), nullable=False)
    quantity = Column(Float, nullable=False)
    cost_price = Column(Float, nullable=False)   # себестоимость за единицу
    sell_price = Column(Float, nullable=False)   # учётная/оценочная цена за единицу
    note = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("StockItem")
