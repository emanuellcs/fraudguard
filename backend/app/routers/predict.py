import json
from typing import List
from fastapi import APIRouter, HTTPException
from app.core.models import TransactionInput, PredictionOutput
from app.services.ml_service import ml_service
from app.core.database import db

router = APIRouter()

@router.post("/predict", response_model=PredictionOutput)
async def predict_fraud(txn: TransactionInput):
    try:
        # Run Inference (CPU bound, fast enough for sync in this demo, but in heavy load we might use run_in_threadpool)
        # We assume the pca_features dict keys are 'V1', 'V2', etc.
        input_dict = txn.dict()
        risk_score, is_fraud = ml_service.predict(input_dict)

        # Log to Database (IO bound - async)
        # We dump the PCA features to JSON string for the DB
        pca_json = json.dumps(txn.pca_features)
        
        txn_id = await db.log_transaction(
            amount=txn.amount,
            time=txn.time,
            pca=pca_json,
            risk_score=risk_score,
            is_fraud=bool(is_fraud)
        )

        return PredictionOutput(
            transaction_id=txn_id,
            risk_score=risk_score,
            is_fraud=bool(is_fraud),
            status="Suspicious" if is_fraud else "Safe"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history", response_model=List[PredictionOutput])
async def get_history(limit: int = 10):
    """
    Fetches the last N transactions + predictions from the DB.
    """
    query = """
        SELECT t.id as transaction_id, p.risk_score, p.prediction_class
        FROM transactions_log t
        JOIN fraud_predictions p ON t.id = p.transaction_id
        ORDER BY t.created_at DESC
        LIMIT $1;
    """
    
    rows = await db.pool.fetch(query, limit)
    
    return [
        PredictionOutput(
            transaction_id=str(r['transaction_id']),
            risk_score=r['risk_score'],
            is_fraud=bool(r['prediction_class']),
            status="Suspicious" if r['prediction_class'] == 1 else "Safe"
        )
        for r in rows
    ]