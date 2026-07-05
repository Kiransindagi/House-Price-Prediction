# EDA Report

## Target Transformation
- Skewness before transformation: 1.88
- Skewness after log1p transformation: 0.12
- **Why Log Transform?** Housing prices are commonly right-skewed. Expensive properties create a long upper tail. Log transformation reduces the influence of extreme values and can improve residual behavior for linear models.

## Multicollinearity (VIF)
- **What VIF measures**: Variance Inflation Factor quantifies the severity of multicollinearity in regression analysis.
- **Why it matters**: Multicollinearity makes coefficients unstable and hard to interpret in linear models. Tree-based models are less affected but can still suffer in feature importance attribution.
|    | Feature      |      VIF |
|---:|:-------------|---------:|
|  0 | LotArea      |  2.39057 |
|  1 | GrLivArea    | 41.7953  |
|  2 | TotalBsmtSF  | 11.3545  |
|  3 | GarageArea   |  9.75341 |
|  4 | OverallQual  | 45.0013  |
|  5 | OverallCond  | 25.7991  |
|  6 | YearBuilt    | 68.0753  |
|  7 | BedroomAbvGr | 27.4517  |
|  8 | TotRmsAbvGrd | 73.111   |