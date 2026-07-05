from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.api.routes import router
from backend.app.core.config import settings
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

figures_dir = os.path.join(os.path.dirname(__file__), "..", "..", "reports", "figures")
os.makedirs(figures_dir, exist_ok=True)
app.mount("/api/figures", StaticFiles(directory=figures_dir), name="figures")

@app.get("/")
def read_root():
    return {"message": "Welcome to the House Price Intelligence API. Please visit /docs for the interactive API documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
