import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import AsyncSessionLocal
from app.models.user import User, Role
from app.core.security import get_password_hash

async def seed_staff():
    async with AsyncSessionLocal() as db:
        # 1. Create Bartender Role
        bt_role_name = "bartender"
        result = await db.execute(select(Role).filter(Role.name == bt_role_name))
        bt_role = result.scalars().first()
        if not bt_role:
            bt_role = Role(name=bt_role_name, description="Бармен", allowed_tabs="Bar,Finance")
            db.add(bt_role)
            await db.commit()
            await db.refresh(bt_role)

        # 2. Create Cook Role
        cook_role_name = "cook"
        result = await db.execute(select(Role).filter(Role.name == cook_role_name))
        cook_role = result.scalars().first()
        if not cook_role:
            cook_role = Role(name=cook_role_name, description="Повар", allowed_tabs="Kitchen")
            db.add(cook_role)
            await db.commit()
            await db.refresh(cook_role)

        # 3. Create Waiter Role
        waiter_role_name = "waiter"
        result = await db.execute(select(Role).filter(Role.name == waiter_role_name))
        waiter_role = result.scalars().first()
        if not waiter_role:
            waiter_role = Role(name=waiter_role_name, description="Официант", allowed_tabs="Waiter")
            db.add(waiter_role)
            await db.commit()
            await db.refresh(waiter_role)

        # 4. Create Bartender User
        user_email = "barmen@resort.com"
        result = await db.execute(select(User).filter(User.email == user_email))
        user = result.scalars().first()
        if not user:
            user = User(
                email=user_email,
                hashed_password=get_password_hash("Barmen123!"),
                full_name="Иван Барменов",
                role_id=bt_role.id,
                is_active=True
            )
            db.add(user)
            await db.commit()
            print("Бармен успешно добавлен!")
        else:
            print("Сотрудник-бармен уже существует.")

        # 5. Create Cook User
        cook_email = "cook@resort.com"
        result = await db.execute(select(User).filter(User.email == cook_email))
        cook_user = result.scalars().first()
        if not cook_user:
            cook_user = User(
                email=cook_email,
                hashed_password=get_password_hash("Cook123!"),
                full_name="Алексей Шеф-Повар",
                role_id=cook_role.id,
                is_active=True
            )
            db.add(cook_user)
            await db.commit()
            print("Повар успешно добавлен!")
        else:
            print("Сотрудник-повар уже существует.")

        # 6. Create Waiter User
        waiter_email = "waiter@resort.com"
        result = await db.execute(select(User).filter(User.email == waiter_email))
        waiter_user = result.scalars().first()
        if not waiter_user:
            waiter_user = User(
                email=waiter_email,
                hashed_password=get_password_hash("Waiter123!"),
                full_name="Сергей Официантов",
                role_id=waiter_role.id,
                is_active=True
            )
            db.add(waiter_user)
            await db.commit()
            print("Официант успешно добавлен!")
        else:
            print("Сотрудник-официант уже существует.")

if __name__ == "__main__":
    asyncio.run(seed_staff())
