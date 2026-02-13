import joblib
import pandas as pd
import logging
from app.core.config import settings

logger = logging.getLogger("uvicorn")

class MLService:
    def __init__(self):
        self.model = None

    def load_model(self):
        logger.info(f"Loading model from {settings.MODEL_PATH}...")
        self.model = joblib.load(settings.MODEL_PATH)
        logger.info("Model loaded successfully.")

    def predict(self, input_data: dict):
        if not self.model:
            raise RuntimeError("Model not loaded")

        # Convert input dict to DataFrame
        # The model expects columns in this order: Time, V1, V2, ..., V28, Amount
        
        # Create data dict with ordered columns
        data = {
            'Time': [input_data['time']],
        }
        
        # Add PCA features in correct order (V1-V28)
        pca_features = input_data.get('pca_features', {})
        for i in range(1, 29):  # V1 to V28
            feature_key = f'V{i}'
            data[feature_key] = [pca_features.get(feature_key, 0.0)]
        
        # Amount comes last
        data['Amount'] = [input_data['amount']]
        
        df = pd.DataFrame(data)
        
        # Predict
        # Pipeline handles scaling automatically
        probability = self.model.predict_proba(df)[0][1] # Probability of Class 1 (Fraud)
        prediction = self.model.predict(df)[0] # 0 or 1
        
        return float(probability), int(prediction)

ml_service = MLService()