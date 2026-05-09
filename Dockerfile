FROM python:3.11-slim

# Prevent .pyc files + ensure logs show properly
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies (important for chromadb, builds, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]