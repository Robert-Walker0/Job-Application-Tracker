from datetime import datetime
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'job_application_tracker_table.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'schema.sql')

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

def add_job_application(application_data: tuple) -> None:
    """
    Inserts a new job application into the database and logs the initial 'Applied' status.

    Args:
        application_data: Tuple containing (company, job_title, date_applied,
        platform, link, pay_type, pay_amount, notes, status, last_heard_from)

    Raises:
        RuntimeError: If the database insert or logging fails.
    """
    application_query = """
    INSERT INTO job_applications(company, job_title, date_applied, platform, link, pay_type, pay_amount, notes, status, last_heard_from)    
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    
    log_query = """
    INSERT INTO job_application_log(application_id, log_date, log_time, event)
    VALUES (?, ?, ?, ?)
    """
    
    connection = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = connection.cursor()        
        cursor.execute(application_query, application_data)
        new_application_id = cursor.lastrowid        
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_time = now.strftime("%H:%M:%S")
        company = application_data[0]
        job_title = application_data[1]
        initial_event = f"Application submitted for {job_title} at {company}."
        cursor.execute(log_query, (new_application_id, current_date, current_time, initial_event))        
        connection.commit()
        
    except sqlite3.Error as error:
        connection.rollback()  # Undo any changes if something fails midway
        raise RuntimeError(f"Failed to add application and history log due to {error}.")
    finally:
        connection.close()


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
        cursor = con.execute(collection_query, (application_id,))
        row = cursor.fetchone()
    except sqlite3.Error as error:
        raise RuntimeError(f"Failed to retrieve application {application_id} due to {error}.")
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
        cursor = con.execute(query)
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
        cursor = con.execute(log_query, (application_id,))
        logs = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as error:
        raise RuntimeError(f"Failed to retrieve logs for application {application_id} due to {error}.")
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
        cursor = con.execute(log_query, (application_id,))
        logs = [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as error:
        raise RuntimeError(f"Failed to retrieve logs for application {application_id} due to {error}.")
    finally:
        con.close()
    
    return logs

if __name__ == '__main__':
    initialize_project_databases()
    print("Database created successfully.")