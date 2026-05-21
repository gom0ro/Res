from app.core.database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)  # 'pool', 'bar', 'room'
    item_name = Column(String)             # e.g. "Бассейн #102" or "Заказ #4 (Бар)" or "Аренда Хамам"
    subtotal = Column(Float, default=0.0)
    service_fee = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    cashier_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    cashier = relationship("User")
