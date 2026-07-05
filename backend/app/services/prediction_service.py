import joblib
import json
import pandas as pd
import numpy as np
from datetime import datetime
from backend.app.core.config import settings
from backend.app.schemas.prediction import PropertyFeatures, PredictionResponse

class PredictionService:
    def __init__(self):
        self.model = None
        self.metadata = None
        
    def load_model(self):
        if self.model is None:
            if settings.MODEL_PATH.exists():
                self.model = joblib.load(settings.MODEL_PATH)
            else:
                raise FileNotFoundError("Model artifact not found.")
                
            if settings.METADATA_PATH.exists():
                with open(settings.METADATA_PATH, "r") as f:
                    self.metadata = json.load(f)
            else:
                self.metadata = {"version": "unknown", "model_name": "unknown"}

    def predict(self, features: PropertyFeatures) -> PredictionResponse:
        self.load_model()
        
        # Convert pydantic model to dataframe
        # Fill missing with mode/median based on schema if needed, but pipeline handles it
        data_dict = features.model_dump()
        df = pd.DataFrame([data_dict])
        
        # Add missing columns based on metadata with NaNs so the pipeline can impute them
        if "features" in self.metadata:
            required_cols = self.metadata["features"]["numerical"] + self.metadata["features"]["categorical"]
            for col in required_cols:
                if col not in df.columns:
                    df[col] = np.nan
        
        # Predict in log space
        X_transformed = self.model.named_steps["preprocessor"].transform(df)
        log_pred = self.model.named_steps["model"].predict(X_transformed)[0]
        
        # Calculate real contributions
        try:
            feature_names = self.model.named_steps["preprocessor"].get_feature_names_out()
        except Exception:
            feature_names = [f"Feature_{i}" for i in range(X_transformed.shape[1])]
            
        coefficients = self.model.named_steps["model"].coef_
        # Ensure it's a 1D array for a single prediction
        input_transformed = X_transformed[0] if len(X_transformed.shape) > 1 else X_transformed
        
        contributions = input_transformed * coefficients
        
        # Build contribution list
        feature_contributions = []
        for name, contrib in zip(feature_names, contributions):
            direction = "positive" if contrib > 0 else "negative" if contrib < 0 else "neutral"
            feature_contributions.append({
                "feature": name.replace("num__", "").replace("cat__", ""),
                "contribution": float(contrib),
                "direction": direction
            })
            
        # Sort and get top positive and negative
        feature_contributions.sort(key=lambda x: x["contribution"], reverse=True)
        top_positive = [f for f in feature_contributions if f["direction"] == "positive"][:5]
        
        feature_contributions.sort(key=lambda x: x["contribution"])
        top_negative = [f for f in feature_contributions if f["direction"] == "negative"][:5]
        
        # Inverse transform
        price_pred = np.expm1(log_pred)
        
        return PredictionResponse(
            predicted_sale_price=float(price_pred),
            model_version=self.metadata.get("version", "unknown"),
            prediction_timestamp=datetime.now().isoformat(),
            top_positive_contributors=top_positive,
            top_negative_contributors=top_negative
        )

prediction_service = PredictionService()
