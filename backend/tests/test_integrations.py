import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    """Root returns app info."""
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["app"] == "SETU"
    assert data["authentication"] == "Clerk"


def test_health():
    """Health check returns healthy."""
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "healthy"
