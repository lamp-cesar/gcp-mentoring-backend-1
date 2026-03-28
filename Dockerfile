# Use slim Python 3.12 image for smaller footprint
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_CREATE=true

# Install system dependencies and Poetry
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install Python dependencies
# Using --no-root to skip installing the package itself, just dependencies
RUN poetry install --no-root

# Copy application files
COPY main.py models.py README.md ./
COPY agents/ ./agents/

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port (Cloud Run uses PORT env var, but this documents the default)
EXPOSE 8080

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application using Poetry
CMD ["poetry", "run", "python", "main.py"]
