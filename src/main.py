"""FastAPI application entry point."""

from fastapi import FastAPI

from src.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)


@app.get("/api/v1/health")
def health() -> dict[str, str]:
    """Liveness check: is the API process up and responding?"""
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
    }