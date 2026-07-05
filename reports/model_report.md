# Model Evaluation Report

## Linear vs Ensemble Comparison
- **Linear Models (Ridge/Lasso)**: Provide clear coefficient interpretations but struggle with non-linear relationships and multicollinearity.
- **Ensemble Models (RF/GB)**: Capture complex non-linearities and interactions better, often leading to lower error, but are black-box models requiring SHAP for explanation.

## Results
- **Ridge**: RMSE=25053.84, MAE=16415.17, R2=0.9182
- **Lasso**: RMSE=25156.00, MAE=16332.02, R2=0.9175
- **RandomForest**: RMSE=28750.83, MAE=17581.10, R2=0.8922
- **GradientBoosting**: RMSE=28950.07, MAE=16794.65, R2=0.8907

## Champion Selection
**Ridge** was selected because it achieved the lowest RMSE (25053.84) on the holdout test set in the original price space.
