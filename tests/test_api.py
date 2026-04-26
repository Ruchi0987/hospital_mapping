from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_suggest_diabetes() -> None:
    response = client.post("/api/suggest", json={"disease": "diabetes"})
    assert response.status_code == 200
    data = response.json()
    assert data["suggestions"]
    assert any("Diabetes" in item["name"] for item in data["suggestions"])
