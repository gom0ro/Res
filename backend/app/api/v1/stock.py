from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List
from app.core.database import get_db
from app.models.stock import StockReceipt, StockItem
from app.schemas.stock import StockReceiptCreate, StockReceiptOut, StockItemCreate

router = APIRouter()

@router.get("/", response_model=List[StockReceiptOut])
async def get_receipts(db: AsyncSession = Depends(get_db)):
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
            product_name=r.product.name if r.product else None,
            product_unit=r.product.unit if r.product else "кг"
        ))
    return out

@router.post("/", response_model=StockReceiptOut)
async def create_receipt(receipt_in: StockReceiptCreate, db: AsyncSession = Depends(get_db)):
    # Check item exists
    item_res = await db.execute(select(StockItem).filter(StockItem.id == receipt_in.product_id))
    item = item_res.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Ингредиент на складе не найден")

    # Update item stock and unit price
    item.stock_quantity += receipt_in.quantity
    item.price = receipt_in.sell_price
    db.add(item)

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
        product_name=item.name,
        product_unit=item.unit
    )

@router.get("/products", response_model=List[dict])
async def get_products_for_stock(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StockItem).filter(StockItem.is_active == True))
    items = result.scalars().all()
    return [{"id": i.id, "name": i.name, "price": i.price, "stock_quantity": i.stock_quantity, "unit": i.unit} for i in items]

@router.post("/items", response_model=dict)
async def create_stock_item(item_in: StockItemCreate, db: AsyncSession = Depends(get_db)):
    # Check if duplicate name
    existing_res = await db.execute(select(StockItem).filter(StockItem.name == item_in.name))
    existing = existing_res.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Ингредиент с таким названием уже существует")

    item = StockItem(
        name=item_in.name,
        unit=item_in.unit,
        price=item_in.price,
        stock_quantity=0.0
    )
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return {"id": item.id, "name": item.name, "unit": item.unit, "price": item.price, "stock_quantity": item.stock_quantity}

