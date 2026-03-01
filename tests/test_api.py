"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture
def client():
    """Create a test client with lifespan support."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def uploaded_dataset(client, sample_csv_path):
    """Upload a sample dataset and return the dataset_id."""
    with open(sample_csv_path, "rb") as f:
        response = client.post("/upload", files={"file": ("sample.csv", f, "text/csv")})
    assert response.status_code == 200
    return response.json()["dataset_id"]


class TestHealthEndpoint:

    def test_health(self, client):
        """Test health check returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestUploadEndpoint:

    def test_upload_csv(self, client, sample_csv_path):
        """Test CSV upload."""
        with open(sample_csv_path, "rb") as f:
            response = client.post("/upload", files={"file": ("sample.csv", f, "text/csv")})
        assert response.status_code == 200
        data = response.json()
        assert "dataset_id" in data
        assert data["rows"] > 0

    def test_upload_wrong_type(self, client, tmp_path):
        """Test error on non-CSV upload."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("hello")
        with open(txt_file, "rb") as f:
            response = client.post("/upload", files={"file": ("test.txt", f, "text/plain")})
        assert response.status_code == 400


class TestAnalysisEndpoint:

    def test_analysis(self, client, uploaded_dataset):
        """Test analysis endpoint."""
        response = client.get(f"/analysis/{uploaded_dataset}")
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "column_stats" in data

    def test_analysis_not_found(self, client):
        """Test 404 on unknown dataset."""
        response = client.get("/analysis/nonexistent")
        assert response.status_code == 404
