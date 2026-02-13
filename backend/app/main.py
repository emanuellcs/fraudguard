from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Add CORS middleware to accept requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}