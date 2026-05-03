from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.database import close_pool
from backend.queue import close_redis


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    yield
    await close_pool()
    await close_redis()


app = FastAPI(title="Infigrate API", lifespan=lifespan)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"service": "infigrate-api"}


@app.get("/health")
def read_health() -> dict[str, str]:
    return {"status": "ok"}
