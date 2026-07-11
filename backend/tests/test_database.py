import pytest
import sqlite3
import database
from datetime import datetime, timedelta

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
    
    first_id = applications[0]["id"]
    logs = database.get_application_logs(first_id)
    assert len(logs) == 1
    assert "Application submitted" in logs[0]["event"]
    assert "log_date" in logs[0]
    assert "log_time" in logs[0]

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

def test_get_application_logs(test_database):
    database.add_job_application(APPLICATION_DATA)
    applications = database.get_all_job_applications()
    first_id = applications[0]["id"]
    
    logs = database.get_application_logs(first_id)
    assert isinstance(logs, list)
    assert len(logs) == 1
    assert logs[0]["event"] == "Application submitted for Software Engineer at Test Company."

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

def test_get_all_job_applications_flags_inactive(test_database):
    """Verifies that SQLite date arithmetic properly tracks and flags apps older than 14 days."""
    today_str = datetime.now().strftime("%Y-%m-%d")
    fifteen_days_ago_str = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")

    fresh_app = (
        "Active Company",
        "Frontend Engineer",
        today_str,
        "LinkedIn",
        "https://example.com",
        "Salaried",
        80000.0,
        "Just applied!",
        "Applied",
        today_str
    )

    stale_app = (
        "Stale Company",
        "Backend Engineer",
        fifteen_days_ago_str,
        "Indeed",
        "https://example.com",
        "Hourly",
        45.0,
        "No response yet...",
        "Applied",
        fifteen_days_ago_str
    )

    database.add_job_application(fresh_app)
    database.add_job_application(stale_app)

    applications = database.get_all_job_applications()
    assert len(applications) == 2

    active_record = next(a for a in applications if a["company"] == "Active Company")
    stale_record = next(a for a in applications if a["company"] == "Stale Company")

    # Assert backend provides integer bitmask indicators (0 = False, 1 = True)
    assert active_record["is_inactive"] == 0
    assert stale_record["is_inactive"] == 1