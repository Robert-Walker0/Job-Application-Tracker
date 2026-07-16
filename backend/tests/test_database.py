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
    "2026-07-07",
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


def test_build_change_log_message_single_change():
    current_row = {"status": "Applied", "notes": "initial Notes"}
    updated_fields = {"status": "Interview"}
    result = database.build_changes_log_message(current_row, updated_fields)
    assert result == "Application updated: Status changed from 'Applied' to 'Interview'"


def test_build_changes_log_message_multiple_changes():
    """Test that multiple changes are separated by semicolons."""
    current_row = {"status": "Applied", "pay_amount": 50.0}
    updated_fields = {"status": "Interview", "pay_amount": 60.0}
    result = database.build_changes_log_message(current_row, updated_fields)
    assert "Status changed from 'Applied' to 'Interview'" in result
    assert "Pay Amount changed from '50.0' to '60.0'" in result
    assert result.startswith("Application updated: ")


def test_build_changes_log_message_no_changes():
    """Test fallback message when no field values are actually altered.

    Notes: This fallback value should never be triggered or used.
    """
    current_row = {"status": "Applied"}
    updated_fields = {"status": "Applied"}
    result = database.build_changes_log_message(current_row, updated_fields)
    assert result == "Application updated (No field values were changed)"


def test_add_initial_log_entry(test_database):
    """Tests adding the inital log entry when creating a job application."""
    conn = database.create_connection()
    cursor = conn.cursor()
    database.add_initial_log_entry(cursor, 101, "Google", "Frontend Lead")
    conn.commit()
    cursor.execute("SELECT * FROM job_application_log WHERE application_id = 101")
    row = cursor.fetchone()
    conn.close()
    assert row is not None
    assert row["application_id"] == 101
    assert row["event"] == "Application submitted for Frontend Lead at Google."
    assert row["log_date"] == datetime.now().strftime("%Y-%m-%d")


def test_log_application_event(test_database):
    """Test helper that handles updating the event history."""
    conn = database.create_connection()
    cursor = conn.cursor()
    test_msg = "Status changed from 'Applied' to 'Interview'"
    database.log_application_event(cursor, 202, test_msg)
    conn.commit()
    cursor.execute("SELECT * FROM job_application_log WHERE application_id = 202")
    row = cursor.fetchone()
    conn.close()
    assert row is not None
    assert row["application_id"] == 202
    assert row["event"] == test_msg
    assert row["log_date"] == datetime.now().strftime("%Y-%m-%d")


def test_add_job_application(test_database):
    """Tests the ability to add a job application."""
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
    """Tests getting a job application from its identification number."""
    database.add_job_application(APPLICATION_DATA)
    applications = database.get_all_job_applications()
    first_id = applications[0]["id"]
    result = database.get_job_application_by_id(first_id)
    assert result["company"] == "Test Company"
    assert result["job_title"] == "Software Engineer"


def test_get_job_application_by_id_not_found(test_database):
    """Tests the ValueError for when the identification number for the job application is not found."""
    with pytest.raises(ValueError):
        database.get_job_application_by_id(99999)


def test_get_all_job_applications(test_database):
    """Tests getting all of the job applications from the database."""
    database.add_job_application(APPLICATION_DATA)
    database.add_job_application(APPLICATION_DATA)
    applications = database.get_all_job_applications()
    assert isinstance(applications, list)
    assert len(applications) == 2


def test_get_all_job_applications_empty(test_database):
    """Tests getting all of the job applications from an empty database."""
    applications = database.get_all_job_applications()
    assert applications == []


def test_get_application_logs(test_database):
    """Tests retrieving the history logs for a specific job application."""
    application_idetification_number = 1
    database.add_job_application(APPLICATION_DATA)
    logs = database.get_application_logs(application_idetification_number)
    assert isinstance(logs, list)
    assert len(logs) == 1
    assert logs[0]["event"] == (
        "Application submitted for Software Engineer at Test Company."
    )


def test_add_job_application_empty_required_field(test_database):
    """Tests adding a job application when mutiple required fields are missing."""
    with pytest.raises(Exception):
        database.add_job_application(
            (
                None,
                "Engineer",
                "2026-07-07",
                None,
                None,
                "Hourly",
                35.0,
                None,
                "Applied",
                "2026-07-07",
            )
        )


def test_add_job_application_invalid_pay_type(test_database):
    """Test adding a job application with an invalid job pay type."""
    with pytest.raises(Exception):
        database.add_job_application(
            (
                "Google",
                "Engineer",
                "2026-07-07",
                None,
                None,
                "InvalidPayType",
                35.0,
                None,
                "Applied",
                "2026-07-07",
            )
        )


def test_add_job_application_invalid_data(test_database):
    """Test adding a job with invalid job application data."""
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
        today_str,
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
        fifteen_days_ago_str,
    )
    database.add_job_application(fresh_app)
    database.add_job_application(stale_app)
    applications = database.get_all_job_applications()
    assert len(applications) == 2
    active_record = next(
        app for app in applications if app["company"] == "Active Company"
    )
    stale_record = next(
        app for app in applications if app["company"] == "Stale Company"
    )
    assert active_record["is_inactive"] == 0
    assert stale_record["is_inactive"] == 1
