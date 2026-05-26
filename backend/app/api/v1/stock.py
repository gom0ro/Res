from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from app.core.database import get_db
from app.core.dependencies import get_current_active_user
from app.models.stock import StockReceipt
from app.models.bar import BarProduct
from app.models.user import User
from app.schemas.stock import StockReceiptCreate, StockReceiptOut

router = APIRouter()

@router.get("/", response_model=List[StockReceiptOut])
async def get_receipts(db: AsyncSession = Depends(get_db), _user: User = Depends(get_current_active_user)):
    result = await db.execute(
        select(StockReceipt)
        .options(selectinload(StockReceipt.product))
        .order_by(StockReceipt.created_at.desc())
    )
    receipts = result.scalars().all()
    out = []
    for r in receipts:
        out.append(StockReceiptOut(
            id=r.id,
            product_id=r.product_id,
            quantity=r.quantity,
            cost_price=r.cost_price,
            sell_price=r.sell_price,
            note=r.note,
            created_at=r.created_at,
            product_name=r.product.name if r.product else None
        ))
    return out

@router.post("/", response_model=StockReceiptOut)
async def create_receipt(receipt_in: StockReceiptCreate, db: AsyncSession = Depends(get_db), _user: User = Depends(get_current_active_user)):
    # Check product exists
    prod_res = await db.execute(select(BarProduct).filter(BarProduct.id == receipt_in.product_id))
    product = prod_res.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")

    # Update product stock and sell price
    product.stock_quantity += receipt_in.quantity
    product.price = receipt_in.sell_price
    db.add(product)

    receipt = StockReceipt(
        product_id=receipt_in.product_id,
        quantity=receipt_in.quantity,
        cost_price=receipt_in.cost_price,
        sell_price=receipt_in.sell_price,
        note=receipt_in.note
    )
    db.add(receipt)
    await db.commit()
    await db.refresh(receipt)

    return StockReceiptOut(
        id=receipt.id,
        product_id=receipt.product_id,
        quantity=receipt.quantity,
        cost_price=receipt.cost_price,
        sell_price=receipt.sell_price,
        note=receipt.note,
        created_at=receipt.created_at,
        product_name=product.name
    )

@router.get("/products", response_model=List[dict])
async def get_products_for_stock(db: AsyncSession = Depends(get_db), _user: User = Depends(get_current_active_user)):
    result = await db.execute(select(BarProduct).filter(BarProduct.is_active == True))
    products = result.scalars().all()
    return [{"id": p.id, "name": p.name, "price": p.price, "stock_quantity": p.stock_quantity} for p in products]
