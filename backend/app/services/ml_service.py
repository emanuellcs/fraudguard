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
        # The pipeline expects columns: 'Time', 'Amount', 'V1', 'V2', ... 'V28'
        
        # Flatten the input
        data = {
            'Time': [input_data['time']],
            'Amount': [input_data['amount']]
        }
        # Merge PCA features (V1-V28)
        data.update({k: [v] for k, v in input_data['pca_features'].items()})
        
        df = pd.DataFrame(data)
        
        # Predict
        # Pipeline handles scaling automatically
        probability = self.model.predict_proba(df)[0][1] # Probability of Class 1 (Fraud)
        prediction = self.model.predict(df)[0] # 0 or 1
        
        return float(probability), int(prediction)

ml_service = MLService()