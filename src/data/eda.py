import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from statsmodels.stats.outliers_influence import variance_inflation_factor

from src.utils.config import DATA_RAW, TARGET_COL, FIGURES_DIR, REPORTS_DIR
from src.utils.logger import get_logger

logger = get_logger(__name__)

def run_eda():
    logger.info("Starting EDA...")
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    df = pd.read_csv(DATA_RAW / "ames_housing.csv")
    
    # 1. Target distribution analysis
    plt.figure(figsize=(10, 5))
    sns.histplot(df[TARGET_COL], kde=True)
    plt.title(f"{TARGET_COL} Distribution")
    plt.savefig(FIGURES_DIR / "target_distribution.png")
    plt.close()
    
    skewness_before = df[TARGET_COL].skew()
    logger.info(f"Target Skewness (Before): {skewness_before:.2f}")
    
    # 2. Log-transformed target
    df["LogSalePrice"] = np.log1p(df[TARGET_COL])
    plt.figure(figsize=(10, 5))
    sns.histplot(df["LogSalePrice"], kde=True)
    plt.title(f"Log1p({TARGET_COL}) Distribution")
    plt.savefig(FIGURES_DIR / "log_target_distribution.png")
    plt.close()
    
    skewness_after = df["LogSalePrice"].skew()
    logger.info(f"Target Skewness (After): {skewness_after:.2f}")
    
    # 3. Multicollinearity / VIF
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    # Remove target, ids, etc for VIF
    features_for_vif = [c for c in numerical_cols if c not in [TARGET_COL, "LogSalePrice", "Id"] and not df[c].isnull().any()]
    
    vif_data = pd.DataFrame()
    X = df[features_for_vif].dropna()
    vif_data["Feature"] = X.columns
    # Calculate VIF for each feature
    # Note: VIF can take time if many features, subsetting to important ones
    core_features = ["LotArea", "GrLivArea", "TotalBsmtSF", "GarageArea", "OverallQual", "OverallCond", "YearBuilt", "BedroomAbvGr", "TotRmsAbvGrd"]
    core_features = [f for f in core_features if f in X.columns]
    
    X_core = X[core_features]
    vif_data = pd.DataFrame()
    vif_data["Feature"] = X_core.columns
    vif_data["VIF"] = [variance_inflation_factor(X_core.values, i) for i in range(len(X_core.columns))]
    
    logger.info(f"VIF Analysis:\n{vif_data}")
    
    # Generate report
    report_path = REPORTS_DIR / "eda_report.md"
    with open(report_path, "w") as f:
        f.write("# EDA Report\n\n")
        f.write("## Target Transformation\n")
        f.write(f"- Skewness before transformation: {skewness_before:.2f}\n")
        f.write(f"- Skewness after log1p transformation: {skewness_after:.2f}\n")
        f.write("- **Why Log Transform?** Housing prices are commonly right-skewed. Expensive properties create a long upper tail. Log transformation reduces the influence of extreme values and can improve residual behavior for linear models.\n\n")
        f.write("## Multicollinearity (VIF)\n")
        f.write("- **What VIF measures**: Variance Inflation Factor quantifies the severity of multicollinearity in regression analysis.\n")
        f.write("- **Why it matters**: Multicollinearity makes coefficients unstable and hard to interpret in linear models. Tree-based models are less affected but can still suffer in feature importance attribution.\n")
        f.write(vif_data.to_markdown())
        
    logger.info("EDA completed successfully.")

if __name__ == "__main__":
    run_eda()
