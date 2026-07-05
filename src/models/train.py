import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
from datetime import datetime

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from src.utils.config import DATA_RAW, TARGET_COL, TEST_SIZE, RANDOM_SEED, MODEL_ARTIFACTS, MODEL_METADATA, REPORTS_DIR
from src.utils.logger import get_logger
from src.features.preprocessing import build_preprocessor
from src.models.evaluate import evaluate_model

logger = get_logger(__name__)

def train_models():
    logger.info("Starting model training pipeline...")
    
    MODEL_ARTIFACTS.mkdir(parents=True, exist_ok=True)
    MODEL_METADATA.mkdir(parents=True, exist_ok=True)
    
    # Load data
    df = pd.read_csv(DATA_RAW / "ames_housing.csv")
    
    # Optional subset for speed if it's very large, but Ames is small (~1460 rows)
    # Define features
    X = df.drop(columns=[TARGET_COL, "Id"], errors="ignore")
    y = np.log1p(df[TARGET_COL])
    
    # Separate columns by type
    num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()
    
    logger.info(f"Numerical features: {len(num_cols)}, Categorical features: {len(cat_cols)}")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED
    )
    
    # Define models
    models = {
        "Ridge": {
            "model": Ridge(random_state=RANDOM_SEED),
            "family": "linear",
            "params": {"model__alpha": [0.1, 1.0, 10.0]}
        },
        "Lasso": {
            "model": Lasso(random_state=RANDOM_SEED),
            "family": "linear",
            "params": {"model__alpha": [0.001, 0.01, 0.1]}
        },
        "RandomForest": {
            "model": RandomForestRegressor(random_state=RANDOM_SEED),
            "family": "tree",
            "params": {"model__n_estimators": [50, 100], "model__max_depth": [None, 10]}
        },
        "GradientBoosting": {
            "model": GradientBoostingRegressor(random_state=RANDOM_SEED),
            "family": "tree",
            "params": {"model__n_estimators": [50, 100], "model__learning_rate": [0.05, 0.1]}
        }
    }
    
    results = {}
    best_model_name = None
    best_score = float('inf')
    best_pipeline = None
    
    for name, config in models.items():
        logger.info(f"Training {name}...")
        preprocessor = build_preprocessor(num_cols, cat_cols, model_family=config["family"])
        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("model", config["model"])
        ])
        
        # Hyperparameter tuning
        search = GridSearchCV(
            pipeline,
            param_grid=config["params"],
            cv=3,
            scoring="neg_mean_squared_error",
            n_jobs=-1
        )
        search.fit(X_train, y_train)
        
        # Evaluate
        y_pred = search.predict(X_test)
        metrics = evaluate_model(y_test, y_pred, is_log_transformed=True)
        results[name] = metrics
        
        logger.info(f"{name} Results: RMSE={metrics['RMSE']:.2f}, MAE={metrics['MAE']:.2f}, R2={metrics['R2']:.4f}")
        
        if metrics["RMSE"] < best_score:
            best_score = metrics["RMSE"]
            best_model_name = name
            best_pipeline = search.best_estimator_
            
    logger.info(f"Champion Model: {best_model_name} with RMSE: {best_score:.2f}")
    
    # Save best model
    joblib.dump(best_pipeline, MODEL_ARTIFACTS / "champion_model.pkl")
    
    # Save metadata
    metadata = {
        "model_name": best_model_name,
        "rmse": best_score,
        "mae": results[best_model_name]["MAE"],
        "r2": results[best_model_name]["R2"],
        "training_date": datetime.now().isoformat(),
        "version": "1.0.0",
        "features": {
            "numerical": num_cols,
            "categorical": cat_cols
        }
    }
    with open(MODEL_METADATA / "model_info.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
    # Generate report
    report_path = REPORTS_DIR / "model_report.md"
    with open(report_path, "w") as f:
        f.write("# Model Evaluation Report\n\n")
        f.write("## Linear vs Ensemble Comparison\n")
        f.write("- **Linear Models (Ridge/Lasso)**: Provide clear coefficient interpretations but struggle with non-linear relationships and multicollinearity.\n")
        f.write("- **Ensemble Models (RF/GB)**: Capture complex non-linearities and interactions better, often leading to lower error, but are black-box models requiring SHAP for explanation.\n\n")
        f.write("## Results\n")
        for name, m in results.items():
            f.write(f"- **{name}**: RMSE={m['RMSE']:.2f}, MAE={m['MAE']:.2f}, R2={m['R2']:.4f}\n")
            
        f.write(f"\n## Champion Selection\n**{best_model_name}** was selected because it achieved the lowest RMSE ({best_score:.2f}) on the holdout test set in the original price space.\n")
        
if __name__ == "__main__":
    train_models()
