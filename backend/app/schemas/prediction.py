from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class PropertyFeatures(BaseModel):
    # SIZE
    LotArea: float = Field(..., ge=0, description="Lot size in square feet")
    GrLivArea: float = Field(..., ge=0, description="Above grade living area in square feet")
    TotalBsmtSF: float = Field(..., ge=0, description="Total square feet of basement area")
    GarageArea: float = Field(..., ge=0, description="Size of garage in square feet")
    
    # QUALITY
    OverallQual: int = Field(..., ge=1, le=10, description="Overall material and finish quality")
    OverallCond: int = Field(..., ge=1, le=10, description="Overall condition rating")
    YearBuilt: int = Field(..., ge=1800, le=2025, description="Original construction date")
    YearRemodAdd: int = Field(..., ge=1800, le=2025, description="Remodel date")
    
    # ROOMS
    BedroomAbvGr: int = Field(..., ge=0, description="Number of bedrooms above basement level")
    FullBath: int = Field(..., ge=0, description="Full bathrooms above grade")
    HalfBath: int = Field(..., ge=0, description="Half baths above grade")
    TotRmsAbvGrd: int = Field(..., ge=0, description="Total rooms above grade (does not include bathrooms)")
    
    # LOCATION (Optional / strings for categorical)
    Neighborhood: str = Field("NAmes", description="Physical locations within Ames city limits")
    MSZoning: str = Field("RL", description="The general zoning classification")
    
    # EXTRAS
    FireplaceQu: Optional[str] = Field("NA", description="Fireplace quality")
    PoolArea: float = Field(0.0, ge=0, description="Pool area in square feet")
    Fence: Optional[str] = Field("NA", description="Fence quality")
    SaleType: str = Field("WD", description="Type of sale")
    SaleCondition: str = Field("Normal", description="Condition of sale")
    
    model_config = ConfigDict(extra="allow")
        
class FeatureContribution(BaseModel):
    feature: str
    contribution: float
    direction: str

class PredictionResponse(BaseModel):
    predicted_sale_price: float
    model_version: str
    prediction_timestamp: str
    explanation_method: str = "Ridge Regression Coefficients (Log Space)"
    top_positive_contributors: list[FeatureContribution] = []
    top_negative_contributors: list[FeatureContribution] = []
