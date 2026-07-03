from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_returns_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_stats_rejects_anonymous():
    resp = client.get("/api/stats")
    assert resp.status_code == 401


def test_stats_rejects_garbage_token():
    resp = client.get("/api/stats", headers={"Authorization": "Bearer not-a-real-jwt"})
    assert resp.status_code in (401, 503)


def test_me_rejects_anonymous():
    resp = client.get("/api/me")
    assert resp.status_code == 401
