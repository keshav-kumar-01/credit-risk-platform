FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p models/trained models/explainers data/raw data/processed reports/outputs reports/figures docs

# Railway uses $PORT env var — default to 8000 if not set
ENV PORT=8000

# Expose port (Railway overrides this with $PORT)
EXPOSE $PORT

# Health check uses the actual port
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:${PORT}/api/v1/health || exit 1

# Start with dynamic port — Railway injects $PORT
CMD uvicorn api.main:app --host 0.0.0.0 --port $PORT
