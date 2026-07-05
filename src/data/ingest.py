import pandas as pd
from sklearn.datasets import fetch_openml
from src.utils.config import DATA_RAW, TARGET_COL
from src.utils.logger import get_logger
from pathlib import Path

logger = get_logger(__name__)

def fetch_and_save_data():
    """Fetches Ames Housing dataset from OpenML and saves it to data/raw."""
    logger.info("Fetching Ames Housing dataset from OpenML...")
    housing = fetch_openml(name="house_prices", as_frame=True, version=1, parser="auto")
    df = housing.frame
    
    # Ensure raw data dir exists
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    raw_path = DATA_RAW / "ames_housing.csv"
    
    df.to_csv(raw_path, index=False)
    logger.info(f"Saved dataset to {raw_path}")
    return raw_path

def load_data(filepath: Path = DATA_RAW / "ames_housing.csv") -> pd.DataFrame:
    """Loads dataset from the raw directory with validations."""
    logger.info(f"Loading data from {filepath}")
    if not filepath.exists():
        logger.error(f"File not found: {filepath}")
        raise FileNotFoundError(f"Missing data file at {filepath}")
        
    df = pd.read_csv(filepath)
    
    if TARGET_COL not in df.columns:
        logger.error(f"Target column '{TARGET_COL}' missing in dataset.")
        raise ValueError(f"Missing target column: {TARGET_COL}")
        
    logger.info(f"Dataset shape: {df.shape}")
    
    missing_pct = df.isnull().mean().mean() * 100
    logger.info(f"Overall missingness: {missing_pct:.2f}%")
    
    return df

if __name__ == "__main__":
    fetch_and_save_data()
