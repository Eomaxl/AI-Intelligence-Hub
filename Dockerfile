# Multi-stage Dockerfile for AI-Layer service
# Python 3.12, optimized for fast builds and small production images
# 
# Stages:
#   base - System deps + Python packages (shared by dev/prod)
#   dev -   Development extras (test deps, hot-reload)
#   prod -  Production image (minimal, non-root user)

#   ---------------------------------------------------------------------
#   Stage 1 : Base - install system dependencies and Python packages
#   ---------------------------------------------------------------------
FROM python:3.12-slim AS base

# Prevent python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1\
    PYTHONUNBUFFERED=1  \
    PIP_NO_CACHE_DIR=1  \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies required by asyncpg, grpcio, and pgvector
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev   \
    curl    \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy depenedency specification first for better layer caching
COPY pyproject.toml ./

# Install production dependencies
RUN pip install --no-cache-dir -e "." 2>/dev/null || pip install --no-cache-dir .

# Copy alembic configuration and migrations
COPY alembic.ini    ./
COPY alembic/   ./alembic/

# Copy application source
COPY ai-layer/ ./ai-layer
COPY protos/ ./protos/
COPY scripts/   ./scripts/

# ----------------------------------------------------------------------------------------
#       Stage 2 : Development - includes test dependencies and dev tools
# ----------------------------------------------------------------------------------------

FROM base AS dev

# Install dev/test dependencies
RUN pip install --no-cache-dir hypothesis pytest pytest-asyncio pytest-cov ruff mypy httpx testcontainers

# Install watchfiles for hot-reload during development
RUN pip install --no-cache-dir watchfiles

# Copy test files
COPY tests/ ./tests/

# Expose ports: HTTP (FastAPI) + gRPC
EXPOSE 8000 50051

# Development entrypoint with hot-reload
CMD ["python", "-m", "uvicorn", "ai_intelligence_hub.service.health:app", \
     "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ─────────────────────────────────────────────────────────────────────────────
# Stage 3: Production — minimal image with non-root user
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS prod

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install only runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copy installed packages from base stage
COPY --from=base /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=base /usr/local/bin /usr/local/bin

# Copy application files from base stage
COPY --from=base /app /app

# Set ownership to non-root user
RUN chown -R appuser:appuser /app

USER appuser

# Expose ports: HTTP (FastAPI) + gRPC
EXPOSE 8000 50051

# Health check
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Production entrypoint
CMD ["python", "-m", "uvicorn", "ai_intelligence_hub.service.health:app", \
     "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
