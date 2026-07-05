import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["model_availability"] == "available"
    
def test_model_info():
    response = client.get("/api/model-info")
    assert response.status_code == 200
    assert "version" in response.json()
    assert "rmse" in response.json()
    
def test_predict_valid():
    payload = {
        "LotArea": 8450,
        "GrLivArea": 1710,
        "TotalBsmtSF": 856,
        "GarageArea": 548,
        "OverallQual": 7,
        "OverallCond": 5,
        "YearBuilt": 2003,
        "YearRemodAdd": 2003,
        "BedroomAbvGr": 3,
        "FullBath": 2,
        "HalfBath": 1,
        "TotRmsAbvGrd": 8,
        "Neighborhood": "CollgCr",
        "MSZoning": "RL",
        "FireplaceQu": "NA",
        "PoolArea": 0,
        "Fence": "NA",
        "SaleType": "WD",
        "SaleCondition": "Normal"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    assert "predicted_sale_price" in response.json()
    assert response.json()["predicted_sale_price"] > 0
    
def test_predict_invalid_negative_area():
    payload = {
        "LotArea": -100, # Invalid
        "GrLivArea": 1710,
        "TotalBsmtSF": 856,
        "GarageArea": 548,
        "OverallQual": 7,
        "OverallCond": 5,
        "YearBuilt": 2003,
        "YearRemodAdd": 2003,
        "BedroomAbvGr": 3,
        "FullBath": 2,
        "HalfBath": 1,
        "TotRmsAbvGrd": 8,
        "Neighborhood": "CollgCr",
        "MSZoning": "RL"
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422 # Pydantic validation error
