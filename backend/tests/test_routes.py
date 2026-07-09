import pytest
from fastapi.testclient import TestClient
import database
from main import app

client = TestClient(app)
ROOT_URL = "/"
APPLICATIONS_URL = "/applications"

@pytest.fixture(autouse=True)
def setup_database(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setattr(database, "DATABASE_PATH", str(db_path))
    database.initialize_project_databases()
    yield


@pytest.fixture
def application_payload():
    return {
        "company": "Test Inc",
        "jobTitle": "Software Engineer",
        "dateApplied": "2026-07-07",
        "platform": "",
        "link": "",
        "payType": "Hourly",
        "payAmount": 35,
        "notes": "",
        "status": "Applied",
        "lastHeardFrom": "2026-07-07"
    }

def test_root():
   response = client.get(ROOT_URL)
   assert response.status_code == 200
   assert response.json()["message"] == "Job Application Tracker API"

def test_get_applications():
    response = client.get(APPLICATIONS_URL)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_application(application_payload):
    response = client.post(APPLICATIONS_URL, json=application_payload)
    assert response.status_code == 201
    assert response.json()["message"] == "Application has been added successfully."

def test_create_application_missing_required_field(application_payload):
    missing_field = "company"
    del application_payload[missing_field]
    response = client.post(APPLICATIONS_URL, json=application_payload)
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert missing_field in detail[0]["loc"]

def test_create_application_invalid_data_type(application_payload):
    invalid_field, invalid_data = "payAmount", "abc"
    application_payload[invalid_field] = invalid_data
    response = client.post(APPLICATIONS_URL, json=application_payload)
    assert response.status_code == 422
    detail = response.json()["detail"]
    assert invalid_field in detail[0]["loc"]    

def test_get_application(application_payload):
    create_response = client.post(APPLICATIONS_URL, json=application_payload)  
    assert create_response.status_code == 201
    all_response = client.get(APPLICATIONS_URL)
    assert all_response.status_code == 200
    applications = all_response.json()
    last_id = applications[-1]["id"]
    response = client.get(f"{APPLICATIONS_URL}/{last_id}")
    assert response.status_code == 200
    assert response.json()["company"] == application_payload["company"]

def test_get_application_not_found():
    app_id = 999999
    response = client.get(f"{APPLICATIONS_URL}/{app_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == f"Application {app_id} not found"

def test_get_application_invalid_id_type():
    response = client.get(f"{APPLICATIONS_URL}/not-a-number")
    assert response.status_code == 422



