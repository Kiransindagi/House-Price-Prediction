import pytest
import pandas as pd
from pathlib import Path
from src.utils.config import TARGET_COL
from src.data.validate import validate_data

def test_config_paths():
    from src.utils.config import PROJECT_ROOT, DATA_RAW
    assert isinstance(PROJECT_ROOT, Path)
    assert isinstance(DATA_RAW, Path)

def test_data_validation():
    # Valid data
    df_valid = pd.DataFrame({
        "SalePrice": [100000, 200000],
        "LotArea": [5000, 6000]
    })
    assert validate_data(df_valid) == True
    
    # Missing target
    df_missing_target = pd.DataFrame({
        "LotArea": [5000, 6000]
    })
    with pytest.raises(KeyError):
        validate_data(df_missing_target)
        
    df_null_target = pd.DataFrame({
        "SalePrice": [100000, None],
        "LotArea": [5000, 6000]
    })
    with pytest.raises(ValueError):
        validate_data(df_null_target)
        
    # Negative area
    df_negative_area = pd.DataFrame({
        "SalePrice": [100000, 200000],
        "LotArea": [5000, -100]
    })
    with pytest.raises(ValueError):
        validate_data(df_negative_area)
