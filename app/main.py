from fastapi import FastAPI

from .core.config import settings
from .routers import auth, billing, customer, milk_collection, milk_rate

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


@app.get("/")
def read_root():
    return {
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "message": "Welcome to the Dairy Hub API",
    }


@app.get("/health")
def health_check():
    return {
        "app_name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "message": "API is healthy and running..",
    }
