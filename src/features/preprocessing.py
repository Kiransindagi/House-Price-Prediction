from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd
import numpy as np

def build_preprocessor(numerical_cols, categorical_cols, model_family="linear"):
    """
    Builds a preprocessing pipeline.
    For linear models, scales numerical features.
    For tree models, numerical scaling is optional but kept for consistency if configured.
    """
    
    # Numerical Pipeline
    num_steps = [
        ("imputer", SimpleImputer(strategy="median"))
    ]
    if model_family == "linear":
        num_steps.append(("scaler", StandardScaler()))
        
    num_pipeline = Pipeline(num_steps)
    
    # Categorical Pipeline
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, numerical_cols),
            ("cat", cat_pipeline, categorical_cols)
        ],
        remainder="drop" # Drop anything not explicitly specified
    )
    
    return preprocessor
