# Dockerfile for python-dairy-hub-api
# Assumes your app entrypoint is `main.py` with a FastAPI app named `app`.

FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable stdout/stderr buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install uv for dependency management
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock /app/

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy application code
COPY . /app

# Create non-root user and give ownership of /app
RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose the port your app uses (FastAPI commonly uses 8000)
EXPOSE 8000

# Default command - run with uvicorn. Adjust workers if needed.
CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
