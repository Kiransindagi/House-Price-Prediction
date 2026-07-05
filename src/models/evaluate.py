import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from src.utils.logger import get_logger

logger = get_logger(__name__)

def evaluate_model(y_true, y_pred, is_log_transformed=True):
    """
    Evaluates predictions. If predictions are in log space,
    inverse transforms them first to compute metrics in original price space.
    """
    if is_log_transformed:
        y_true_orig = np.expm1(y_true)
        y_pred_orig = np.expm1(y_pred)
    else:
        y_true_orig = y_true
        y_pred_orig = y_pred
        
    rmse = np.sqrt(mean_squared_error(y_true_orig, y_pred_orig))
    mae = mean_absolute_error(y_true_orig, y_pred_orig)
    r2 = r2_score(y_true_orig, y_pred_orig)
    
    metrics = {
        "RMSE": rmse,
        "MAE": mae,
        "R2": r2
    }
    
    return metrics
