import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import AsyncSessionLocal, engine, Base
from app.models.user import User, Role
from app.core.security import get_password_hash
from app.core.config import settings

# Import all models so Base.metadata includes all tables
import app.models  # noqa: F401

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # Create roles
        default_roles = {
            "admin": "Dashboard,Pool,Loungers,Bar,Steam,Finance,Kitchen,Staff,Analytics,Stock",
            "reception": "Pool,Loungers,Steam",
            "waiter": "Waiter",
            "bartender": "Bar,Finance",
            "cashier": "Finance",
            "manager": "Dashboard,Pool,Loungers,Bar,Steam,Finance,Kitchen,Staff,Analytics,Stock",
            "cook": "Kitchen"
        }
        for role_name, tabs in default_roles.items():
            result = await db.execute(select(Role).filter(Role.name == role_name))
            role = result.scalars().first()
            if not role:
                db.add(Role(name=role_name, allowed_tabs=tabs))
        
        await db.commit()

        # Create admin user
        result = await db.execute(select(Role).filter(Role.name == "admin"))
        admin_role = result.scalars().first()
        
        result = await db.execute(select(User).filter(User.email == settings.ADMIN_EMAIL))
        admin = result.scalars().first()
        
        if not admin:
            admin = User(
                email=settings.ADMIN_EMAIL,
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                full_name=settings.ADMIN_FULL_NAME,
                role_id=admin_role.id,
                is_active=True
            )
            db.add(admin)
            await db.commit()
            print("Admin user created successfully")
        else:
            print("Admin user already exists")

        # Seed default loungers if empty
        from app.models.lounger import Lounger
        l_res = await db.execute(select(Lounger).limit(1))
        if l_res.scalars().first() is None:
            for i in range(1, 13):
                db.add(Lounger(number=f"T-{i}", zone="main", price_per_hour=3000))
            for i in range(1, 5):
                db.add(Lounger(number=f"V-{i}", zone="vip", price_per_hour=8000))
            await db.commit()
            print("Default loungers seeded successfully")

        # Seed default spa/vip rooms if empty
        from app.models.steam import Room, RoomType, RoomStatus
        r_res = await db.execute(select(Room).limit(1))
        if r_res.scalars().first() is None:
            db.add(Room(name="Хамам Лакшери", room_type=RoomType.STEAM_ROOM, price_per_hour=5000, status=RoomStatus.FREE))
            db.add(Room(name="Финская Сауна", room_type=RoomType.STEAM_ROOM, price_per_hour=4000, status=RoomStatus.FREE))
            db.add(Room(name="VIP Кабина №1", room_type=RoomType.VIP_CABIN, price_per_hour=10000, status=RoomStatus.FREE))
            db.add(Room(name="VIP Кабина №2", room_type=RoomType.VIP_CABIN, price_per_hour=10000, status=RoomStatus.FREE))
            db.add(Room(name="Русская Баня на дровах", room_type=RoomType.STEAM_ROOM, price_per_hour=6000, status=RoomStatus.FREE))
            await db.commit()
            print("Default rooms seeded successfully")

        # Seed default bar categories & products if empty
        from app.models.bar import BarCategory, BarProduct
        bc_res = await db.execute(select(BarCategory).limit(1))
        if bc_res.scalars().first() is None:
            drinks = BarCategory(name="Напитки")
            db.add(drinks)
            snacks = BarCategory(name="Закуски")
            db.add(snacks)
            general = BarCategory(name="Общее")
            db.add(general)
            await db.flush()

            p1 = BarProduct(name="Coca-Cola 0.5", price=500, stock_quantity=100, category_id=drinks.id)
            p2 = BarProduct(name="Fanta 0.5", price=500, stock_quantity=100, category_id=drinks.id)
            p3 = BarProduct(name="Чипсы Lays", price=800, stock_quantity=50, category_id=snacks.id)
            p4 = BarProduct(name="Сендвич с курицей", price=1200, stock_quantity=20, category_id=snacks.id)
            p5 = BarProduct(name="Пиво Разливное 0.5", price=1500, stock_quantity=200, category_id=drinks.id)
            db.add_all([p1, p2, p3, p4, p5])
            await db.commit()
            print("Default bar products seeded successfully")

if __name__ == "__main__":
    print("Initializing database...")
    asyncio.run(init_db())
    print("Database initialization complete.")
