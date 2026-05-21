from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    position: Optional[int] = 0

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config: from_attributes = True

class ProductBase(BaseModel):
    name: str
    price: float
    stock_quantity: int = 0
    barcode: Optional[str] = None
    is_active: bool = True
    category_id: Optional[int] = None

class ProductCreate(ProductBase): pass

class Product(ProductBase):
    id: int
    class Config: from_attributes = True
