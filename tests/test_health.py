from fastapi.testclient import TestClient

import src.main
from src.main import app

client = TestClient(app)


def fake_checks(**overrides):
    """Build a fake check_all that reports every dependency up, except overrides."""
    results = {"database": True, "opensearch": True, "ollama": True, **overrides}

    async def fake_check_all():
        return results

    return fake_check_all


def test_health_ok_when_all_dependencies_up(monkeypatch):
    monkeypatch.setattr(src.main, "check_all", fake_checks())

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"] == body["opensearch"] == body["ollama"] == "ok"


def test_health_503_when_one_dependency_down(monkeypatch):
    monkeypatch.setattr(src.main, "check_all", fake_checks(ollama=False))

    response = client.get("/api/v1/health")

    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "degraded"
    assert body["ollama"] == "unreachable"
    assert body["database"] == "ok"