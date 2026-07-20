import pytest
from unittest.mock import patch

from app import create_app


@pytest.fixture
def client():
    app = create_app("development")
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"IT401" in response.data
    assert b"Web Intelligence" in response.data


def test_about(client):
    catalog_course = {
        "title": "IT 401 - Web Intelligence",
        "units": "3",
        "meeting_format": "Three hours of lecture in the lab per week",
        "prerequisite": "IT 380",
        "description": "Official catalog description.",
        "grading": "Letter Grade",
        "catalog": "2026-2027 Catalog",
    }
    with patch("routes.main.fetch_catalog_course", return_value=catalog_course):
        response = client.get("/about")

    assert response.status_code == 200
    assert b"IT401" in response.data
    assert b"Web Intelligence" in response.data
    assert b"Official catalog description." in response.data
    assert b"Live catalog data" in response.data


def test_stats(client):
    github_stats = {
        "repo_name": "bpthoms/it401_project_template",
        "stars": 7,
        "language": "Python",
    }
    with patch("routes.main.fetch_github_stats", return_value=github_stats):
        response = client.get("/stats")

    assert response.status_code == 200
    assert b"bpthoms/it401_project_template" in response.data
    assert b">7<" in response.data
    assert b"Python" in response.data
    assert b"API connected" in response.data
