from pydantic import BaseModel, Field
from typing import List

class TransactionInput(BaseModel):
    time: float = Field(..., description="Seconds elapsed since first transaction")
    amount: float = Field(..., gt=0, description="Transaction amount")
    # V1-V28 are PCA features. We accept them as a list/vector for simplicity in JSON or as individual fields. Let's use a dictionary/map for flexibility.
    pca_features: dict = Field(..., description="Dictionary of V1 to V28")

class PredictionOutput(BaseModel):
    transaction_id: str
    risk_score: float
    is_fraud: bool
    status: str