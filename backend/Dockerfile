FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port (Railway uses $PORT env var)
EXPOSE 8000

# Run application - Railway will inject PORT
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}