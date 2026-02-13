from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import predict
from app.services.ml_service import ml_service
from app.core.database import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    ml_service.load_model()
    await db.connect()
    yield
    # Shutdown
    await db.disconnect()

app = FastAPI(title="FraudGuard API", lifespan=lifespan)

app.include_router(predict.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}