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

if __name__ == "__main__":
    print("Initializing database...")
    asyncio.run(init_db())
    print("Database initialization complete.")
