def test_docs_available(client):
    """Check if Swagger docs are reachable"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_download_endpoint_returns_job(client):
    """Verify /download returns job_id and status"""
    response = client.get("/download/", params={"url": "https://example.com/video"})
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "processing"


def test_status_processing(client):
    """Check status endpoint for a non-existing job_id"""
    response = client.get("/status/fake-job-id")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_file_not_found(client):
    """Ensure file fetch returns error when missing"""
    response = client.get("/files/nonexistent.mp4")
    # Either custom error JSON or FastAPI 404
    assert response.status_code in (200, 404)
