import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fraud Detection API"
    DATABASE_URL: str  # e.g. postgresql://user:pass@host:5432/postgres
    MODEL_PATH: str = "/app/models/fraud_detection_pipeline.pkl"

    class Config:
        env_file = ".env"

settings = Settings()