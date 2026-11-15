from unittest.mock import Mock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_job_validation():
    response = client.post("/api/jobs", json={"source_url": "https://example.com/video", "min_seconds": 90, "max_seconds": 60})
    assert response.status_code == 422

def test_job_submission(monkeypatch):
    task = Mock(id="task-test")
    monkeypatch.setattr("app.main.process_source.delay", Mock(return_value=task))
    response = client.post("/api/jobs", json={"source_url": "https://example.com/video"})
    assert response.status_code == 202
    assert response.json()["task_id"] == "task-test"
    assert response.json()["status"] == "submitted"
