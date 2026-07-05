import os
from pathlib import Path

class Settings:
    PROJECT_NAME: str = "House Price Intelligence API"
    VERSION: str = "1.0.0"
    MODEL_PATH: Path = Path(__file__).resolve().parent.parent.parent.parent / "models" / "artifacts" / "champion_model.pkl"
    METADATA_PATH: Path = Path(__file__).resolve().parent.parent.parent.parent / "models" / "metadata" / "model_info.json"

settings = Settings()
