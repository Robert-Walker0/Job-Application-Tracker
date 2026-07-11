from fastapi import status
import pytest, os

os.environ["FRONTEND_REMOTE_URL"] = "https://www.example.com"

from fastapi.testclient import TestClient
import database, json, io
from main import app

client = TestClient(app)
ROOT_URL = "/"
APPLICATIONS_URL = "/applications"

IMPORT_URL = "/applications/import/json"


VALID_APPLICATIONS = [
    {
        "company": "Google",
        "jobTitle": "Software Engineer",
        "dateApplied": "2026-07-07",
        "platform": "LinkedIn",
        "link": "https://google.com",
        "payType": "Salaried",
        "payAmount": 120000,
        "notes": "Great opportunity",
        "status": "Applied",
        "lastHeardFrom": "2026-07-07"
    },
    {
        "company": "Affirm",
        "jobTitle": "Apprentice Engineer",
        "dateApplied": "2026-07-08",
        "platform": "Company Website",
        "link": "https://affirm.com",
        "payType": "Salaried",
        "payAmount": 95000,
        "notes": "",
        "status": "Applied",
        "lastHeardFrom": "2026-07-08"
    }
]


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
   assert response.status_code == status.HTTP_200_OK
   assert response.json()["message"] == "Job Application Tracker API"

def test_get_applications():
    response = client.get(APPLICATIONS_URL)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_create_application(application_payload):
    response = client.post(APPLICATIONS_URL, json=application_payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["message"] == "Application has been added successfully."

def test_create_application_missing_required_field(application_payload):
    missing_field = "company"
    del application_payload[missing_field]
    response = client.post(APPLICATIONS_URL, json=application_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    detail = response.json()["detail"]
    assert missing_field in detail[0]["loc"]

def test_create_application_invalid_data_type(application_payload):
    invalid_field, invalid_data = "payAmount", "abc"
    application_payload[invalid_field] = invalid_data
    response = client.post(APPLICATIONS_URL, json=application_payload)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    detail = response.json()["detail"]
    assert invalid_field in detail[0]["loc"]    

def test_get_application(application_payload):
    create_response = client.post(APPLICATIONS_URL, json=application_payload)  
    assert create_response.status_code == status.HTTP_201_CREATED
    all_response = client.get(APPLICATIONS_URL)
    assert all_response.status_code == status.HTTP_200_OK
    applications = all_response.json()
    last_id = applications[-1]["id"]
    response = client.get(f"{APPLICATIONS_URL}/{last_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["company"] == application_payload["company"]

def test_get_application_not_found():
    app_id = 999999
    response = client.get(f"{APPLICATIONS_URL}/{app_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == f"Application {app_id} not found"

def test_get_application_invalid_id_type():
    response = client.get(f"{APPLICATIONS_URL}/not-a-number")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_export_applications_json_success(monkeypatch):
    """Test that exporting data returns the correct headers and data payload."""
    mock_data = [
        {"id": 1, "company_name": "Google", "job_title": "Software Engineer"}
    ]
    monkeypatch.setattr("routes.applications.database.get_all_job_applications", lambda: mock_data)
    monkeypatch.setattr("routes.applications.to_camel_case_dict", lambda x: x)
    filename = "my_custom_backup"
    response = client.get(f"/applications/export/json?filename={filename}")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/json"   
    assert response.headers["content-disposition"] == f'attachment; filename="{filename}.json"' or \
           response.headers["content-disposition"] == f'attachment; filename={filename}.json'
    json_data = response.json()
    assert len(json_data) == 1
    assert json_data[0]["company_name"] == "Google"


def test_export_applications_json_empty_database(monkeypatch):
    """Test that a 404 is raised with a clear message when no jobs exist."""
    monkeypatch.setattr("routes.applications.database.get_all_job_applications", lambda: [])
    response = client.get("/applications/export/json")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No job applications found to export."

def make_json_file(data, filename="applications.json"):
    """Helper that creates an in-memory JSON file for upload testing."""
    content = json.dumps(data).encode("utf-8")
    return {"file": (filename, io.BytesIO(content), "application/json")}


def test_import_valid_json_file():
    response = client.post(IMPORT_URL, files=make_json_file(VALID_APPLICATIONS))
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["message"] == "Import complete. 2 imported, 0 failed."


def test_import_verifies_data_in_database():
    client.post(IMPORT_URL, files=make_json_file(VALID_APPLICATIONS))
    applications = database.get_all_job_applications()
    assert len(applications) == 2
    assert applications[0]["company"] == "Google"
    assert applications[1]["company"] == "Affirm"


def test_import_invalid_file_type():
    content = b"company,job_title\nGoogle,Engineer"
    response = client.post(IMPORT_URL, files={
        "file": ("applications.csv", io.BytesIO(content), "text/csv")
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Only .json files are accepted" in response.json()["detail"]


def test_import_invalid_json():
    content = b"this is not valid json {"
    response = client.post(IMPORT_URL, files={
        "file": ("applications.json", io.BytesIO(content), "application/json")
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid JSON file" in response.json()["detail"]


def test_import_wrong_structure():
    content = json.dumps({"company": "Google"}).encode("utf-8")
    response = client.post(IMPORT_URL, files={
        "file": ("applications.json", io.BytesIO(content), "application/json")
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Expected a list" in response.json()["detail"]


def test_import_empty_list():
    response = client.post(IMPORT_URL, files=make_json_file([]))
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["message"] == "Import complete. 0 imported, 0 failed."


def test_import_partial_failure():
    mixed_data = [
        VALID_APPLICATIONS[0],
        {
            "company": None,
            "job_title": None,
            "date_applied": None,
            "platform": None,
            "link": None,
            "pay_type": "InvalidType",
            "pay_amount": None,
            "notes": None,
            "status": None,
            "last_heard_from": None
        }
    ]
    response = client.post(IMPORT_URL, files=make_json_file(mixed_data))
    assert response.status_code == status.HTTP_201_CREATED
    assert "1 imported" in response.json()["message"]
    assert "1 failed" in response.json()["message"]