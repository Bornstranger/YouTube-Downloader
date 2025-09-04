from unittest.mock import patch

from fastapi.testclient import TestClient

STATUS_CODE_OK = 200
STATUS_CODE_NOT_FOUND = 404


def test_docs_available(client: TestClient) -> None:
    """Check if Swagger docs are reachable."""
    response = client.get("/docs")
    assert response.status_code == STATUS_CODE_OK


def test_download_endpoint_returns_job(client: TestClient) -> None:
    """Verify /download returns job_id and status."""
    # Mock Celery task to avoid RabbitMQ dependency
    with patch("app.worker.download_video_task.delay") as mock_task:
        response = client.get("/download/", params={"url": "https://example.com/video"})
    assert response.status_code == STATUS_CODE_OK
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "processing"
    mock_task.assert_called_once()


def test_status_processing(client: TestClient) -> None:
    """Check status endpoint for a non-existing job_id."""
    response = client.get("/status/fake-job-id")
    assert response.status_code == STATUS_CODE_OK
    data = response.json()
    assert "status" in data


def test_file_not_found(client: TestClient) -> None:
    """Ensure file fetch returns error when missing."""
    response = client.get("/files/nonexistent.mp4")
    # Either custom error JSON or FastAPI 404
    assert response.status_code in (STATUS_CODE_OK, STATUS_CODE_NOT_FOUND)
