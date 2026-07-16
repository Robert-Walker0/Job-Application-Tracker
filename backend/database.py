from datetime import datetime
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "job_application_tracker_table.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")


def initialize_project_databases() -> None:
    """Creates all database tables from schema.sql if they don't exist.

    Safe to call on every startup, uses if NOT EXISTS in schema.
    """
    connection = sqlite3.connect(DATABASE_PATH)
    with open(SCHEMA_PATH) as file:
        connection.executescript(file.read())
    connection.commit()
    connection.close()


def create_connection() -> sqlite3.Connection:
    """Creates and returns a configured SQLite database connection.

    Set row_factory to sqlite3.Row so rows can be accessed by
    column name and converted to dictionaries with dict(row).

    Returns:
        connection: a sqlite3.Connection configured database connection.
    """
    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row
    return connection


def add_initial_log_entry(
    cursor: sqlite3.Cursor, application_id: int, company: str, job_title: str
) -> None:
    """Writes the initial submission log entry for a new application."""
    current_time = datetime.now()
    log_date = current_time.strftime("%Y-%m-%d")
    log_time = current_time.strftime("%H:%M:%S")
    event = f"Application submitted for {job_title} at {company}."
    log_query = """
    INSERT INTO job_application_log(application_id, log_date, log_time, event)
    VALUES (?, ?, ?, ?)
    """
    cursor.execute(log_query, (application_id, log_date, log_time, event))


def log_application_event(
    cursor: sqlite3.Cursor, application_id: int, event_message: str
) -> None:
    """Write a custom event log entry to the history table using an active cursor."""
    current_time = datetime.now()
    log_date = current_time.strftime("%Y-%m-%d")
    log_time = current_time.strftime("%H:%M:%S")
    history_query = """
    INSERT INTO job_application_log (application_id, event, log_date, log_time)
    VALUES (?, ?, ?, ?) 
    """
    cursor.execute(history_query, (application_id, event_message, log_date, log_time))


def build_changes_log_message(current_row: dict, updated_fields: dict) -> str:
    changed_pieces = []
    for key, new_value in updated_fields.items():
        old_value = current_row[key]
        str_old = (
            "None"
            if old_value is None or str(old_value).strip() == ""
            else str(old_value).strip()
        )
        str_new = (
            "None"
            if new_value is None or str(new_value).strip() == ""
            else str(new_value).strip()
        )

        if str_old != str_new:
            friendly_field_name = " ".join(word.capitalize() for word in key.split("_"))
            changed_pieces.append(
                f"{friendly_field_name} changed from '{str_old}' to '{str_new}'"
            )

    if changed_pieces:
        return f"Application updated: {'; '.join(changed_pieces)}"
    return "Application updated (No field values were changed)"  # This result should be impossible due to REACT Frotnend setup along with backend code, but we should notre if this ever happens somehow.


def add_job_application(application_data: tuple, history: list = None) -> int:
    """
    Inserts a new job application into the database and logs the initial 'Applied' status.

    Args:
    application_data: Tuple containing (company, job_title, date_applied,
    platform, link, pay_type, pay_amount, notes, status, last_heard_from)

    Raise:
    RuntimeError: If the database insert or logging fails.
    """
    application_query = """
    INSERT INTO job_applications(company, job_title, date_applied, platform, link, pay_type, pay_amount, notes, status, last_heard_from)    
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.cursor()
        cursor.execute(application_query, application_data)
        current_app_id = cursor.lastrowid

        if not history:
            company = application_data[0]
            job_title = application_data[1]
            add_initial_log_entry(cursor, current_app_id, company, job_title)
        else:
            for entry in history:
                log_data = [entry.get(key) for key in ("log_date", "log_time", "event")]
                log_query = """
                INSERT INTO job_application_log (application_id, log_date, log_time, event)
                VALUES (?, ?, ?, ?)
                """
                cursor.execute(log_query, (current_app_id, *log_data))

        connection.commit()

    return current_app_id


def get_job_application_by_id(application_id: int) -> dict:
    """Retrieves a job application from the database by its ID number.

    Args:
        application_id: The unique ID (int) of the application to retrieve.

    Returns:
        job_application: The job application matching the given ID.

    Raises:
        ValueError: If the application was not found or does not exist.

    """
    collection_query = "SELECT * FROM job_applications WHERE id = ?"
    con = create_connection()
    try:
        cursor = con.cursor()
        cursor.execute(collection_query, (application_id,))
        row = cursor.fetchone()
    except sqlite3.Error as error:
        raise RuntimeError(
            f"Failed to retrieve application {application_id} due to {error}."
        )
    finally:
        con.close()

    if not row:
        raise ValueError(f"No application found with the id: {application_id}")

    job_application = dict(row)
    return job_application


def get_all_job_applications() -> list:
    """Retrieves all of the job applications from the database and dynamically flags inactive ones using SQLite dae arithmetic.

    Returns:
        job_applications: A list of all job applications as dictionary,
        or an empty list if no applications exist.

    Raises:
        RunTimeError: If the database query fails
    """
    query = """
    SELECT *, 
           CASE 
               WHEN status = 'Applied' AND (julianday('now') - julianday(date_applied)) >= 14 
               THEN 1 
               ELSE 0 
           END as is_inactive
    FROM job_applications
    """
    con = create_connection()
    try:
        cursor = con.cursor()
        cursor.execute(query)
        applications = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as error:
        raise RuntimeError(f"Failed to fetch applications: {error}")
    finally:
        con.close()

    return applications


def get_application_logs(application_id: int) -> list:
    """Retrieves all history logs for a specific application, ordered oldest to newest.

    Args:
        application_id: The unique ID (int) of the application whose logs to fetch.

    Returns:
        logs: A list of dictionaries containing 'log_date' and 'event' keys.

    Raises:
        RuntimeError: If the database query fails.
    """
    log_query = """
    SELECT log_date, log_time, event 
    FROM job_application_log 
    WHERE application_id = ? 
    ORDER BY datetime(log_date || ' ' || log_time) ASC
    """
    con = create_connection()
    try:
        cursor = con.cursor()
        cursor.execute(log_query, (application_id,))
        logs = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as error:
        raise RuntimeError(
            f"Failed to retrieve logs for application {application_id} due to {error}."
        )
    finally:
        con.close()

    return logs


def get_application_logs(application_id: int) -> list:
    """Retrieves all history logs for a specific application, ordered oldest to newest.

    Args:
        application_id: The unique ID (int) of the application whose logs to fetch.

    Returns:
        logs: A list of dictionaries containing 'log_date' and 'event' keys.

    Raises:
        RuntimeError: If the database query fails.
    """
    log_query = """
    SELECT log_date, log_time, event 
    FROM job_application_log 
    WHERE application_id = ? 
    ORDER BY datetime(log_date || ' ' || log_time) ASC
    """
    con = create_connection()
    try:
        cursor = con.cursor()
        cursor.execute(log_query, (application_id,))
        logs = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as error:
        raise RuntimeError(
            f"Failed to retrieve logs for application {application_id} due to {error}."
        )
    finally:
        con.close()

    return logs


def update_job_application(application_id: int, updated_fields: dict) -> dict:
    """Updates an existing job application and logs a detailed [Field] changed from [Old] to [New] history message."""

    connection = create_connection()
    try:
        cursor = connection.cursor()
        current_data_query = "SELECT * FROM job_applications WHERE id = ?"
        current_row = cursor.execute(current_data_query, (application_id,)).fetchone()
        if not current_row:
            raise ValueError(f"No application found with the id: {application_id}")
        event_message = build_changes_log_message(current_row, updated_fields)
        columns = ", ".join(f"{key} = ?" for key in updated_fields.keys())
        values = list(updated_fields.values())
        values.append(application_id)
        update_query = f"UPDATE job_applications SET {columns} WHERE id = ?"
        cursor.execute(update_query, values)
        log_application_event(cursor, application_id, event_message)
        connection.commit()
    except sqlite3.Error as error:
        connection.rollback()
        raise RuntimeError(
            f"Failed to update application {application_id} due to {error}."
        )
    finally:
        connection.close()
    return get_job_application_by_id(application_id)


if __name__ == "__main__":
    initialize_project_databases()
    print("Database created successfully.")
