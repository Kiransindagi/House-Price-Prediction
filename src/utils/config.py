from pathlib import Path

# Project Roots
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Data Directories
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

# Model Directories
MODEL_ARTIFACTS = PROJECT_ROOT / "models" / "artifacts"
MODEL_METADATA = PROJECT_ROOT / "models" / "metadata"

# Reports
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# ML Config
TARGET_COL = "SalePrice"
RANDOM_SEED = 42
TEST_SIZE = 0.2
CV_FOLDS = 5
