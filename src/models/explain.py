import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from src.utils.config import DATA_RAW, MODEL_ARTIFACTS, FIGURES_DIR, TARGET_COL
from src.utils.logger import get_logger

logger = get_logger(__name__)

def generate_explanations():
    logger.info("Generating model explanations using SHAP...")
    
    # Load model and data
    model_path = MODEL_ARTIFACTS / "champion_model.pkl"
    if not model_path.exists():
        logger.error("Champion model not found.")
        return
        
    pipeline = joblib.load(model_path)
    df = pd.read_csv(DATA_RAW / "ames_housing.csv")
    X = df.drop(columns=[TARGET_COL, "Id"], errors="ignore")
    
    # Take a sample for SHAP to avoid long computation
    X_sample = X.sample(100, random_state=42)
    
    # We need to transform the data first because the pipeline contains preprocessor
    # However, SHAP TreeExplainer requires the underlying tree model and the transformed data
    # We can use KernelExplainer for the whole pipeline, but it's slow.
    # Let's try to extract the model.
    preprocessor = pipeline.named_steps['preprocessor']
    model = pipeline.named_steps['model']
    
    X_transformed = preprocessor.transform(X_sample)
    
    # Get feature names if possible
    # scikit-learn >= 1.0 has get_feature_names_out
    try:
        feature_names = preprocessor.get_feature_names_out()
    except:
        feature_names = [f"Feature_{i}" for i in range(X_transformed.shape[1])]
        
    # Check if tree model for TreeExplainer
    if type(model).__name__ in ["RandomForestRegressor", "GradientBoostingRegressor"]:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_transformed)
    else:
        # Linear models
        explainer = shap.LinearExplainer(model, X_transformed)
        shap_values = explainer.shap_values(X_transformed)
        
    # Generate SHAP summary plot
    plt.figure(figsize=(10, 8))
    shap.summary_plot(shap_values, features=X_transformed, feature_names=feature_names, show=False)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "shap_summary.png")
    plt.close()
    
    logger.info("SHAP explanations generated and saved.")

if __name__ == "__main__":
    generate_explanations()
