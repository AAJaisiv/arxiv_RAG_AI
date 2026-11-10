"""FastAPI application entry point."""

from fastapi import FastAPI, Response, status

from src.config import get_settings
from src.health import check_all

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.1",
)


@app.get("/api/v1/health")
async def health(response: Response) -> dict[str, str]:
    """Readiness check: is the API up AND able to reach every dependency?"""
    checks = await check_all()
    all_ok = all(checks.values())

    if not all_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": "ok" if all_ok else "degraded",
        "service": settings.app_name,
        "environment": settings.environment,
        **{name: "ok" if ok else "unreachable" for name, ok in checks.items()},
    }