from fastapi import status
import pytest
from fastapi.testclient import TestClient
import database, services, utility_functions, json, io
from main import app

client = TestClient(app)
ROOT_URL = "/"
APPLICATIONS_URL = "/applications"
EXPORT_URL = "/applications/export/json"
IMPORT_URL = "/applications/import/json"


VALID_APPLICATIONS = [
    {
        "company": "Google",
        "jobTitle": "Software Engineer",
        "location": "400 4th Avenue Jackson Heights, NY 11372",
        "priority": "High",
        "workType": "On-Site",
        "dateApplied": "2026-07-07",
        "platform": "LinkedIn",
        "link": "https://google.com",
        "payType": "Salaried",
        "payAmount": 120000,
        "resumeName": "",
        "notes": "Great opportunity",
        "status": "Applied",
        "lastHeardFrom": "2026-07-07",
    },
    {
        "company": "Affirm",
        "jobTitle": "Apprentice Engineer",
        "location": "400 4th Avenue Jackson Heights, NY 11372",
        "priority": "High",
        "workType": "On-Site",
        "dateApplied": "2026-07-08",
        "platform": "Company Website",
        "link": "https://affirm.com",
        "payType": "Salaried",
        "payAmount": 95000,
        "resumeName": "",
        "notes": "",
        "status": "Applied",
        "lastHeardFrom": "2026-07-08",
    },
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
        "location": "400 4th Avenue Jackson Heights, NY 11372",
        "priority": "Medium",
        "workType": "On-Site",
        "dateApplied": "2026-07-07",
        "platform": "",
        "link": "",
        "payType": "Hourly",
        "payAmount": 35,
        "resumeName": "",
        "notes": "",
        "status": "Applied",
        "lastHeardFrom": "2026-07-07",
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
    assert isinstance(response.json()["id"], int)


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


def test_export_applications_json_success():
    """Test that exporting data returns the correct headers and data payload."""
    create_response = client.post(APPLICATIONS_URL, json=VALID_APPLICATIONS[0])
    application_id = create_response.json()["id"]
    filename = "my_custom_backup"
    response = client.get(f"{EXPORT_URL}?filename={filename}")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/json"
    assert (
        response.headers["content-disposition"]
        == f'attachment; filename="{filename}.json"'
        or response.headers["content-disposition"]
        == f"attachment; filename={filename}.json"
    )
    json_data = response.json()
    assert len(json_data) == 1
    assert json_data[0]["id"] == application_id
    assert json_data[0]["company"] == "Google"


def test_export_applications_json_empty_database(monkeypatch):
    """Test that a 404 is raised with a clear message when no jobs exist."""
    monkeypatch.setattr(
        "routes.applications.database.get_all_job_applications", lambda: []
    )
    response = client.get(EXPORT_URL)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No job applications found to export."


def test_import_valid_json_file():
    response = client.post(
        IMPORT_URL, files=utility_functions.make_json_file(VALID_APPLICATIONS)
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["message"] == "Import complete. 2 imported, 0 failed."


def test_import_verifies_data_in_database():
    client.post(IMPORT_URL, files=utility_functions.make_json_file(VALID_APPLICATIONS))
    applications = database.get_all_job_applications()
    assert len(applications) == 2
    assert applications[0]["company"] == "Google"
    assert applications[1]["company"] == "Affirm"


def test_import_invalid_file_type():
    content = b"company,job_title\nGoogle,Engineer"
    response = client.post(
        IMPORT_URL,
        files={"file": ("applications.csv", io.BytesIO(content), "text/csv")},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Only .json files are accepted" in response.json()["detail"]


def test_import_invalid_json():
    content = b"this is not valid json {"
    response = client.post(
        IMPORT_URL,
        files={"file": ("applications.json", io.BytesIO(content), "application/json")},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid JSON file" in response.json()["detail"]


def test_import_wrong_structure():
    response = client.post(
        IMPORT_URL, files=utility_functions.make_json_file({"company": "Google"})
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Expected a list" in response.json()["detail"]


def test_import_empty_list():
    response = client.post(IMPORT_URL, files=utility_functions.make_json_file([]))
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["message"] == "Import complete. 0 imported, 0 failed."


def test_process_application_import_handles_partial_failures():
    mixed_data = [
        {
            "company": "Valid Corp",
            "jobTitle": "Backend Engineer",
            "location": "400 4th Avenue Jackson Heights, NY 11372",
            "priority": "High",
            "workType": "On-Site",
            "dateApplied": "2026-07-15",
            "platform": "LinkedIn",
            "link": "https://linkedin.com/jobs/1",
            "payType": "Salaried",
            "payAmount": "100000",
            "resumeName": "",
            "notes": "First round soon",
            "status": "Applied",
            "lastHeardFrom": "2026-07-15",
            "history": [
                {
                    "log_date": "2026-07-15",
                    "log_time": "12:00:00",
                    "event": "Applied via LinkedIn",
                }
            ],
        },
        {
            "company": "Invalid Corp",
            "jobTitle": "Frontend Engineer",
            "dateApplied": "2026-07-15",
            "platform": "Indeed",
            "link": "https://indeed.com/jobs/2",
            "payType": "InvalidType",
            "payAmount": "50",
            "notes": "Should fail",
            "status": "Applied",
            "lastHeardFrom": "2026-07-15",
        },
    ]
    response = client.post(
        IMPORT_URL, files=utility_functions.make_json_file(mixed_data)
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "1 imported" in response.json()["message"]
    assert "1 failed" in response.json()["message"]


def test_update_job_application_by_id(application_payload):
    create_response = client.post(APPLICATIONS_URL, json=application_payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    all_response = client.get(APPLICATIONS_URL)
    application_id = all_response.json()[-1]["id"]
    response = client.put(
        f"{APPLICATIONS_URL}/{application_id}",
        json={"company": "Updated Company", "status": "Interview"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["company"] == "Updated Company"
    assert response.json()["status"] == "Interview"


def test_update_job_application_by_id_not_found():
    response = client.put(
        f"{APPLICATIONS_URL}/99999", json={"company": "Updated Company"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "99999" in response.json()["detail"]


def test_update_job_application_by_id_no_fields(application_payload):
    create_response = client.post(APPLICATIONS_URL, json=application_payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    all_response = client.get(APPLICATIONS_URL)
    application_id = all_response.json()[-1]["id"]
    response = client.put(f"{APPLICATIONS_URL}/{application_id}", json={})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_job_application_by_id_logs_history(application_payload):
    create_response = client.post(APPLICATIONS_URL, json=application_payload)
    assert create_response.status_code == status.HTTP_201_CREATED
    application_id = create_response.json()["id"]
    client.put(f"{APPLICATIONS_URL}/{application_id}", json={"status": "Interview"})
    history_response = client.get(f"{APPLICATIONS_URL}/{application_id}/history")
    assert history_response.status_code == status.HTTP_200_OK
    history = history_response.json()
    assert len(history) > 0
    assert any("Status" in entry["event"] for entry in history)


def test_delete_application_success():
    response = client.post(APPLICATIONS_URL, json=VALID_APPLICATIONS[0])
    application_id = response.json()["id"]

    response = client.delete(f"{APPLICATIONS_URL}/{application_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == application_id


def test_delete_application_not_found():
    response = client.delete(f"{APPLICATIONS_URL}/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_all_applications():
    create_response = [
        client.post(APPLICATIONS_URL, json=VALID_APPLICATIONS[0]),
        client.post(APPLICATIONS_URL, json=VALID_APPLICATIONS[1]),
    ]

    assert all(response.status_code == 201 for response in create_response)
    assert all("id" in response.json() for response in create_response)

    delete_response = client.delete(f"{APPLICATIONS_URL}/all")
    assert delete_response.status_code == status.HTTP_200_OK
    response = client.get(APPLICATIONS_URL)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_delete_all_applications_then_404_on_old_id():
    create_responses = [
        client.post(APPLICATIONS_URL, json=VALID_APPLICATIONS[0]),
        client.post(APPLICATIONS_URL, json=VALID_APPLICATIONS[1]),
    ]
    application_ids = [r.json()["id"] for r in create_responses]

    delete_response = client.delete(f"{APPLICATIONS_URL}/all")
    assert delete_response.status_code == status.HTTP_200_OK

    for application_id in application_ids:
        response = client.get(f"{APPLICATIONS_URL}/{application_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_application_removes_rounds_and_history_via_cascade():
    response = client.post(APPLICATIONS_URL, json=VALID_APPLICATIONS[0])
    application_id = response.json()["id"]

    client.post(
        f"{APPLICATIONS_URL}/{application_id}/interview-rounds",
        json={"roundLabel": "Phone Screen", "roundDate": "2026-07-20", "notes": ""},
    )

    rounds_before = client.get(f"{APPLICATIONS_URL}/{application_id}/interview-rounds")
    history_before = client.get(f"{APPLICATIONS_URL}/{application_id}/history")
    assert len(rounds_before.json()) > 0
    assert len(history_before.json()) > 0

    delete_response = client.delete(f"{APPLICATIONS_URL}/{application_id}")
    assert delete_response.status_code == status.HTTP_200_OK

    rounds_after = client.get(f"{APPLICATIONS_URL}/{application_id}/interview-rounds")
    history_after = client.get(f"{APPLICATIONS_URL}/{application_id}/history")
    assert rounds_after.status_code == status.HTTP_404_NOT_FOUND
    assert history_after.status_code == status.HTTP_404_NOT_FOUND
