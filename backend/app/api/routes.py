from fastapi import APIRouter, HTTPException, Depends
from backend.app.schemas.prediction import PropertyFeatures, PredictionResponse
from backend.app.services.prediction_service import prediction_service

router = APIRouter()

@router.get("/health")
def health_check():
    try:
        prediction_service.load_model()
        model_status = "available"
        version = prediction_service.metadata.get("version", "unknown")
    except Exception as e:
        model_status = "unavailable"
        version = "unknown"
        
    return {
        "status": "ok",
        "model_availability": model_status,
        "model_version": version
    }

@router.get("/model-info")
def model_info():
    try:
        prediction_service.load_model()
        return prediction_service.metadata
    except Exception as e:
        raise HTTPException(status_code=503, detail="Model artifact unavailable")

@router.post("/predict", response_model=PredictionResponse)
def predict_price(features: PropertyFeatures):
    try:
        return prediction_service.predict(features)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
