from app.core.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class StockReceipt(Base):
    __tablename__ = "stock_receipts"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("bar_products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    cost_price = Column(Float, nullable=False)   # себестоимость за единицу
    sell_price = Column(Float, nullable=False)   # цена продажи за единицу
    note = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("BarProduct")
