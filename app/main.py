from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import init_db
from app.routers.advertisement import router as advertisement_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Advertisements Service",
    description="Сервис объявлений купли/продажи",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(advertisement_router)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Advertisements API is running"}
