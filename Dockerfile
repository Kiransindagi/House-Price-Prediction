FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and models
COPY backend/ ./backend/
COPY src/ ./src/
COPY models/artifacts/ ./models/artifacts/
COPY models/metadata/ ./models/metadata/
COPY data/ ./data/
COPY reports/ ./reports/

# Expose port
EXPOSE 8000

# Run API
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
