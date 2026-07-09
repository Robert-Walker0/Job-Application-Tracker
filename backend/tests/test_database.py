import pytest
import sqlite3
import database

APPLICATION_DATA = (
    "Test Company",
    "Software Engineer",
    "2026-07-07",
    "LinkedIn",
    "https://example.com",
    "Hourly",
    35.0,
    "Test notes",
    "Applied",
    "2026-07-07"
)

@pytest.fixture
def test_database(tmp_path, monkeypatch):
    db_path = tmp_path / "test_database.db"
    monkeypatch.setattr(database, "DATABASE_PATH", str(db_path))
    database.initialize_project_databases()
    yield db_path


def test_initialize_project_database_creates_tables(test_database):
    conn = sqlite3.connect(str(test_database))
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    assert "job_applications" in tables
    assert "interview_rounds" in tables
    assert "job_application_log" in tables


def test_create_connection_returns_connection(test_database):
    conn = database.create_connection()
    assert isinstance(conn, sqlite3.Connection)
    assert conn.row_factory == sqlite3.Row
    conn.close()

def test_add_job_application(test_database):
    database.add_job_application(APPLICATION_DATA)
    applications = database.get_all_job_applications()
    assert len(applications) == 1
    assert applications[0]["company"] == "Test Company"

def test_get_job_application_by_id(test_database):
    database.add_job_application(APPLICATION_DATA)
    applications = database.get_all_job_applications()
    first_id = applications[0]["id"]
    result = database.get_job_application_by_id(first_id)
    assert result["company"] == "Test Company"
    assert result["job_title"] == "Software Engineer"


def test_get_job_application_by_id_not_found(test_database):
    with pytest.raises(ValueError):
        database.get_job_application_by_id(99999)


def test_get_all_job_applications(test_database):
    database.add_job_application(APPLICATION_DATA)
    database.add_job_application(APPLICATION_DATA)
    applications = database.get_all_job_applications()
    assert isinstance(applications, list)
    assert len(applications) == 2


def test_get_all_job_applications_empty(test_database):
    applications = database.get_all_job_applications()
    assert applications == []

def test_add_job_application_empty_required_field(test_database):
    with pytest.raises(Exception):
        database.add_job_application((
            None,  
            "Engineer",
            "2026-07-07",
            None,
            None,
            "Hourly",
            35.0,
            None,
            "Applied",
            "2026-07-07"
        ))

def test_add_job_application_invalid_pay_type(test_database):
    with pytest.raises(Exception):
        database.add_job_application((
            "Google",
            "Engineer",
            "2026-07-07",
            None,
            None,
            "InvalidPayType",
            35.0,
            None,
            "Applied",
            "2026-07-07"
        ))

def test_add_job_application_invalid_data(test_database):
    with pytest.raises(Exception):
        database.add_job_application(("only", "three", "values"))
