import json
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