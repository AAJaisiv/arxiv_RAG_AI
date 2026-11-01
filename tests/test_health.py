from fastapi.testclient import TestClient

import src.main
from src.main import app

client = TestClient(app)


def test_health_ok_when_database_up(monkeypatch):
    monkeypatch.setattr(src.main, "check_database", lambda: True)

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["database"] == "ok"


def test_health_503_when_database_down(monkeypatch):
    monkeypatch.setattr(src.main, "check_database", lambda: False)

    response = client.get("/api/v1/health")

    assert response.status_code == 503
    assert response.json()["status"] == "degraded"
    assert response.json()["database"] == "unreachable"