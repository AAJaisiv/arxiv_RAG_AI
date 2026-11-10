"""Dependency health checks. Each check returns True if the dependency is usable."""

import asyncio
import logging

import httpx

from src.config import get_settings
from src.db import check_database

logger = logging.getLogger(__name__)

settings = get_settings()


async def check_opensearch(client: httpx.AsyncClient) -> bool:
    """OpenSearch is usable if its cluster status is green or yellow."""
    try:
        response = await client.get(f"{settings.opensearch_host}/_cluster/health")
        response.raise_for_status()
        return response.json().get("status") in {"green", "yellow"}
    except (httpx.HTTPError, ValueError):
        logger.exception("OpenSearch health check failed")
        return False


async def check_ollama(client: httpx.AsyncClient) -> bool:
    """Ollama is usable if its server answers."""
    try:
        response = await client.get(f"{settings.ollama_host}/api/version")
        response.raise_for_status()
        return True
    except httpx.HTTPError:
        logger.exception("Ollama health check failed")
        return False


async def check_all() -> dict[str, bool]:
    """Run all checks at the same time and collect the results."""
    async with httpx.AsyncClient(timeout=3.0) as client:
        database, opensearch, ollama = await asyncio.gather(
            asyncio.to_thread(check_database),
            check_opensearch(client),
            check_ollama(client),
        )
    return {"database": database, "opensearch": opensearch, "ollama": ollama}