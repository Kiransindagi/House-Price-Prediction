import os
from pathlib import Path

dirs = [
    "data/raw",
    "data/processed",
    "models/artifacts",
    "models/metadata",
    "reports/figures",
    "src/data",
    "src/features",
    "src/models",
    "src/utils",
    "tests",
    "backend/app/api",
    "backend/app/core",
    "backend/app/schemas",
    "backend/app/services",
    "backend/tests",
    "frontend/src/components",
    "frontend/src/pages",
    "frontend/src/services",
    "notebooks"
]

init_files = [
    "src/__init__.py",
    "src/data/__init__.py",
    "src/features/__init__.py",
    "src/models/__init__.py",
    "src/utils/__init__.py",
    "tests/__init__.py",
    "backend/__init__.py",
    "backend/app/__init__.py",
    "backend/app/api/__init__.py",
    "backend/app/core/__init__.py",
    "backend/app/schemas/__init__.py",
    "backend/app/services/__init__.py"
]

for d in dirs:
    Path(d).mkdir(parents=True, exist_ok=True)

for f in init_files:
    Path(f).touch(exist_ok=True)

print("Project structure created successfully.")
