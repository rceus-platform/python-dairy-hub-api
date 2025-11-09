FROM python:3.11-slim


# Prevent Python from writing .pyc files and enable stdout/stderr buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Install build dependencies (only what pip might need)
RUN apt-get update \
&& apt-get install -y --no-install-recommends build-essential gcc \
&& rm -rf /var/lib/apt/lists/*


WORKDIR /app


# Install Python dependencies
# Make sure you have a requirements.txt at the project root.
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
&& pip install --no-cache-dir -r /app/requirements.txt


# Copy application code
COPY . /app


# Create non-root user and give ownership of /app
RUN useradd --create-home appuser \
&& chown -R appuser:appuser /app
USER appuser


# Expose the port your app uses (FastAPI commonly uses 8000)
EXPOSE 8000


# Default command - run with uvicorn. Adjust workers if needed.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
