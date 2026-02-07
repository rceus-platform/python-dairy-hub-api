"""FastAPI application entrypoint."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.routers import auth, billing, customer, milk_collection, milk_rate

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(milk_collection.router, prefix=settings.API_V1_STR)
app.include_router(milk_rate.router, prefix=settings.API_V1_STR)
app.include_router(billing.router, prefix=settings.API_V1_STR)
app.include_router(customer.router, prefix=settings.API_V1_STR)

# Mount static files (admin login UI)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/admin", StaticFiles(directory=static_dir, html=True), name="admin")


@app.get("/")
def read_root():
    """Return basic metadata and navigation hints."""
    return {
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "message": "Welcome to the Dairy Hub API",
        "admin_portal": "/admin",
        "api_docs": "/docs",
    }


@app.get("/health")
def health_check():
    """Return service health information."""
    return {
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "message": "API is healthy and running..",
    }
