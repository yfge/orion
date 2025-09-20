FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app/backend

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy backend project
COPY backend /app/backend

# Install backend in a venv-less image
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

EXPOSE 8000

# Default env (override in compose)
ENV ORION_DATABASE_URL="sqlite:///./orion.db" \
    ORION_SECRET_KEY="dev-secret" \
    ORION_PUBLIC_API_KEY="dev-public-key" \
    ORION_CORS_ORIGINS="*"

# Run migrations then start API
CMD sh -c "alembic upgrade head && uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"

