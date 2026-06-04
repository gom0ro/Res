from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.core.database import get_db
from app.models.bar import BarCategory, BarProduct
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.bar import Category, CategoryCreate, Product as ProductSchema, ProductCreate
from app.schemas.order import Order as OrderSchema, OrderCreate

router = APIRouter()

@router.post("/seed")
async def seed_bar(db: AsyncSession = Depends(get_db)):
    # Clear existing products and categories first to allow clean re-seeding
    from sqlalchemy import delete
    await db.execute(delete(BarProduct))
    await db.execute(delete(BarCategory))
    await db.commit()

    # Create category "Напитки"
    drinks = BarCategory(name="Напитки")
    db.add(drinks)

    # Create category "Закуски"
    snacks = BarCategory(name="Закуски")
    db.add(snacks)

    # Flush session to generate IDs
    await db.flush()

    # Create products
    p1 = BarProduct(name="Coca-Cola 0.5", price=500, stock_quantity=100, category_id=drinks.id)
    p2 = BarProduct(name="Fanta 0.5", price=500, stock_quantity=100, category_id=drinks.id)
    p3 = BarProduct(name="Чипсы Lays", price=800, stock_quantity=50, category_id=snacks.id)
    p4 = BarProduct(name="Сендвич с курицей", price=1200, stock_quantity=20, category_id=snacks.id)
    p5 = BarProduct(name="Пиво Разливное 0.5", price=1500, stock_quantity=200, category_id=drinks.id)
    
    db.add_all([p1, p2, p3, p4, p5])
    await db.commit()
    return {"msg": "Bar seeded successfully"}

@router.get("/products", response_model=List[ProductSchema])
async def get_products(include_inactive: bool = False, db: AsyncSession = Depends(get_db)):
    if include_inactive:
        result = await db.execute(select(BarProduct))
    else:
        result = await db.execute(select(BarProduct).filter(BarProduct.is_active == True))
    products = result.scalars().all()
    # Dynamic stock quantity from StockItem if matching name exists
    from app.models.stock import StockItem
    for p in products:
        item_res = await db.execute(select(StockItem).filter(StockItem.name == p.name))
        item = item_res.scalars().first()
        if item:
            p.stock_quantity = int(item.stock_quantity)
        else:
            p.stock_quantity = None
    return products

@router.post("/products", response_model=ProductSchema)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    category_id = product_in.category_id
    if not category_id:
        # Check if default category exists
        cat_res = await db.execute(select(BarCategory).filter(BarCategory.name == "Общее"))
        category = cat_res.scalars().first()
        if not category:
            category = BarCategory(name="Общее")
            db.add(category)
            await db.flush()
        category_id = category.id

    product = BarProduct(
        name=product_in.name,
        price=product_in.price,
        stock_quantity=product_in.stock_quantity,
        barcode=product_in.barcode,
        is_active=product_in.is_active,
        category_id=category_id
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

@router.put("/products/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: int, 
    product_in: ProductCreate, 
    db: AsyncSession = Depends(get_db)
):
    res = await db.execute(select(BarProduct).filter(BarProduct.id == product_id))
    product = res.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
        
    product.name = product_in.name
    product.price = product_in.price
    product.stock_quantity = product_in.stock_quantity if product_in.stock_quantity is not None else 0
    product.barcode = product_in.barcode
    product.is_active = product_in.is_active
    product.category_id = product_in.category_id
    
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product

@router.delete("/products/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(BarProduct).filter(BarProduct.id == product_id))
    product = res.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
        
    # Check if the product is in any active orders
    active_orders_query = await db.execute(
        select(Order)
        .join(OrderItem)
        .filter(
            OrderItem.product_id == product_id,
            Order.status.in_([OrderStatus.NEW, OrderStatus.PREPARING, OrderStatus.READY])
        )
    )
    active_order = active_orders_query.scalars().first()
    if active_order:
        raise HTTPException(
            status_code=400,
            detail="Нельзя удалить блюдо, так как оно находится в активных заказах на кухне"
        )
        
    await db.delete(product)
    await db.commit()
    return {"msg": "Товар успешно удален из меню"}

@router.get("/categories", response_model=List[Category])
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(BarCategory).order_by(BarCategory.position.asc()))
    return result.scalars().all()

@router.post("/categories", response_model=Category)
async def create_category(category_in: CategoryCreate, db: AsyncSession = Depends(get_db)):
    # Check if category with this name already exists
    exist_res = await db.execute(select(BarCategory).filter(BarCategory.name == category_in.name))
    if exist_res.scalars().first():
        raise HTTPException(status_code=400, detail="Категория с таким названием уже существует")
    
    # Get max position to append to end
    pos_res = await db.execute(select(BarCategory))
    all_cats = pos_res.scalars().all()
    max_pos = max([c.position for c in all_cats]) if all_cats else -1
    
    category = BarCategory(
        name=category_in.name,
        description=category_in.description,
        color=category_in.color or "#4B5563",
        icon=category_in.icon or "🍽️",
        position=max_pos + 1
    )
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category

@router.put("/categories/reorder")
async def reorder_categories(category_ids: List[int], db: AsyncSession = Depends(get_db)):
    for index, cat_id in enumerate(category_ids):
        res = await db.execute(select(BarCategory).filter(BarCategory.id == cat_id))
        category = res.scalars().first()
        if category:
            category.position = index
            db.add(category)
    await db.commit()
    return {"msg": "Порядок категорий успешно обновлен"}

@router.put("/categories/{category_id}", response_model=Category)
async def update_category(category_id: int, category_in: CategoryCreate, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(BarCategory).filter(BarCategory.id == category_id))
    category = res.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    # Check if name is taken by another category
    if category.name != category_in.name:
        exist_res = await db.execute(
            select(BarCategory)
            .filter(BarCategory.name == category_in.name)
            .filter(BarCategory.id != category_id)
        )
        if exist_res.scalars().first():
            raise HTTPException(status_code=400, detail="Категория с таким названием уже существует")
            
    category.name = category_in.name
    category.description = category_in.description
    category.color = category_in.color
    category.icon = category_in.icon
    category.position = category_in.position
    
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category

@router.delete("/categories/{category_id}")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(BarCategory).filter(BarCategory.id == category_id))
    category = res.scalars().first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    # Check if there are any products in this category
    prod_res = await db.execute(select(BarProduct).filter(BarProduct.category_id == category_id))
    if prod_res.scalars().first():
        raise HTTPException(
            status_code=400, 
            detail="Нельзя удалить категорию, содержащую товары. Сначала переместите или удалите товары."
        )
    
    await db.delete(category)
    await db.commit()
    return {"msg": "Категория успешно удалена"}

# --- ORDERS ---
@router.post("/orders", response_model=OrderSchema)
async def create_bar_order(order_in: OrderCreate, db: AsyncSession = Depends(get_db)):
    if not order_in.items:
        raise HTTPException(status_code=400, detail="Корзина пуста")

    subtotal = 0.0
    order_items_to_add = []

    # Process each order item
    for item in order_in.items:
        prod_res = await db.execute(select(BarProduct).filter(BarProduct.id == item.product_id))
        product = prod_res.scalars().first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Товар с ID {item.product_id} не найден")
        
        # Check stock quantity from StockItem if there is a matching StockItem
        from app.models.stock import StockItem
        item_res = await db.execute(select(StockItem).filter(StockItem.name == product.name))
        stock_item = item_res.scalars().first()
        
        if stock_item:
            current_stock = stock_item.stock_quantity
            if current_stock < item.quantity:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Недостаточно товара '{product.name}' на складе. Доступно: {current_stock}"
                )
            # Deduct stock
            stock_item.stock_quantity -= item.quantity
            db.add(stock_item)
        else:
            # Cooked dish / unlimited stock item - no deduction and no check!
            pass

        # Calculate pricing
        price_at_time = product.price
        subtotal += price_at_time * item.quantity

        # Create OrderItem object
        order_item = OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            price_at_time=price_at_time
        )
        order_items_to_add.append(order_item)

    # Compute fees: 10% only for delivery to lounger, 0% for self-pickup
    service_fee_percentage = 10.0 if order_in.lounger_id is not None else 0.0
    service_fee = round(subtotal * (service_fee_percentage / 100.0))
    total_amount = subtotal + service_fee

    # Create main Order record
    is_paid = order_in.lounger_id is None
    order = Order(
        status=OrderStatus.COMPLETED if is_paid else OrderStatus.NEW,
        waiter_id=order_in.waiter_id,
        lounger_id=order_in.lounger_id,
        subtotal=subtotal,
        service_fee_percentage=service_fee_percentage,
        service_fee=service_fee,
        total_amount=total_amount,
        is_paid=is_paid
    )
    
    # Associate items
    for item_obj in order_items_to_add:
        order.items.append(item_obj)
        
    db.add(order)
    
    # Register transaction if paid
    if is_paid:
        from app.models.finance import Transaction
        txn = Transaction(
            category="bar",
            item_name="Бар: заказ у стойки",
            subtotal=subtotal,
            service_fee=service_fee,
            total_amount=total_amount
        )
        db.add(txn)
        
    await db.commit()
    await db.refresh(order)

    # Reload with relationships
    result = await db.execute(
        select(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product)
        )
        .filter(Order.id == order.id)
    )
    return result.scalars().first()

@router.get("/orders", response_model=List[OrderSchema])
async def get_bar_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product)
        )
        .order_by(Order.created_at.desc())
    )
    return result.scalars().all()

@router.post("/orders/{order_id}/status", response_model=OrderSchema)
async def update_order_status(
    order_id: int, 
    status: OrderStatus, 
    is_paid: Optional[bool] = None, 
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product)
        )
        .filter(Order.id == order_id)
    )
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
        
    order.status = status
    if is_paid is not None:
        if is_paid and not order.is_paid:
            from app.models.finance import Transaction
            txn = Transaction(
                category="bar",
                item_name=f"Бар: заказ #{order.id} к топчану T-{order.lounger_id or ''}",
                subtotal=order.subtotal,
                service_fee=order.service_fee,
                total_amount=order.total_amount
            )
            db.add(txn)
        order.is_paid = is_paid
        
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order
