import asyncio
from apps.db.database import engine
from apps.db.base import Base
from fastapi import FastAPI
from contextlib import asynccontextmanager
from apps.db.database import engine
from apps.routers.auth import user_router, appointment_router


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(appointment_router)
