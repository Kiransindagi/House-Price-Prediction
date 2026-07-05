import pandas as pd
from src.utils.logger import get_logger

logger = get_logger(__name__)

def validate_data(df: pd.DataFrame, target_col: str = "SalePrice"):
    """Validates the dataset for training requirements."""
    logger.info("Starting data validation...")
    
    # 1. Missing target
    if df[target_col].isnull().any():
        logger.error(f"Target column '{target_col}' contains missing values.")
        raise ValueError(f"Target '{target_col}' cannot contain missing values.")
    
    # 2. Impossible negative values
    area_features = ["LotArea", "GrLivArea", "TotalBsmtSF", "GarageArea"]
    for feature in area_features:
        if feature in df.columns and (df[feature] < 0).any():
            logger.error(f"Feature '{feature}' contains impossible negative values.")
            raise ValueError(f"Negative physical areas are not allowed: {feature}")
    
    # 3. Duplicate records
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        logger.warning(f"Found {duplicates} duplicate rows. Consider dropping them.")
    
    # 4. Constant columns
    constant_cols = [col for col in df.columns if df[col].nunique() <= 1]
    if constant_cols:
        logger.warning(f"Found constant columns: {constant_cols}")
        
    logger.info("Data validation passed.")
    return True
