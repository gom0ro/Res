from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base

# Import all models so Base.metadata knows about all tables
import app.models  # noqa: F401

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Resort Complex Management Dashboard API",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Ideally use Alembic for migrations in production.
    # We create tables here for rapid development if they don't exist.
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # uncomment to reset db
        await conn.run_sync(Base.metadata.create_all)

    try:
        from init_db import init_db
        await init_db()
    except Exception as e:
        print(f"Error during startup DB initialization: {e}")

@app.get("/")
async def root():
    return {"message": "Welcome to Resort Dashboard API"}

from app.api.v1 import api_router

app.include_router(api_router, prefix="/api/v1")

