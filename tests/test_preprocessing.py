import pytest
import pandas as pd
import numpy as np
from src.features.preprocessing import build_preprocessor
from src.models.evaluate import evaluate_model

def test_preprocessing_pipeline():
    df = pd.DataFrame({
        "num1": [1.0, 2.0, np.nan, 4.0],
        "cat1": ["A", "B", "A", None]
    })
    
    num_cols = ["num1"]
    cat_cols = ["cat1"]
    
    # Test linear family (should scale)
    preprocessor_lin = build_preprocessor(num_cols, cat_cols, model_family="linear")
    X_trans_lin = preprocessor_lin.fit_transform(df)
    assert not np.isnan(X_trans_lin).any(), "NaNs should be imputed"
    
    # Check shape: num1 (1), cat1 (2 categories after imputing mode "A")
    # Actually most_frequent of "A", "B", "A", None is "A".
    # Categories: "A", "B".
    assert X_trans_lin.shape[1] >= 3
    
def test_evaluate_model():
    # log space predictions
    y_true_log = np.log1p(np.array([100000, 200000]))
    y_pred_log = np.log1p(np.array([110000, 190000]))
    
    metrics = evaluate_model(y_true_log, y_pred_log, is_log_transformed=True)
    
    assert "RMSE" in metrics
    assert "MAE" in metrics
    assert "R2" in metrics
    
    # Check MAE is exactly 10000
    assert metrics["MAE"] == pytest.approx(10000.0)
