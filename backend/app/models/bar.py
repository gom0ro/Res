from app.core.database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey

class BarCategory(Base):
    __tablename__ = "bar_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    color = Column(String, nullable=True)
    icon = Column(String, nullable=True)
    position = Column(Integer, default=0)

class BarProduct(Base):
    __tablename__ = "bar_products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("bar_categories.id"))
    name = Column(String, index=True)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    barcode = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, default=True)
