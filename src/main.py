"""FastAPI application entry point."""

from fastapi import FastAPI, Response, status

from src.config import get_settings
from src.db import check_database

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)


@app.get("/api/v1/health")
def health(response: Response) -> dict[str, str]:
    """Readiness check: is the API up AND able to reach its database?"""
    database_ok = check_database()

    if not database_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": "ok" if database_ok else "degraded",
        "service": settings.app_name,
        "environment": settings.environment,
        "database": "ok" if database_ok else "unreachable",
    }