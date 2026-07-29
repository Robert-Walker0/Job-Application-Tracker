from pydantic import ValidationError
from models import JobApplication
from typing import List, Dict, Tuple
import utility_functions
import sqlite3
import database


def build_export_record(app: Dict) -> Dict:
    """Builds one application's full export record, including history and rounds.

    Args:
        app (Dict): One raw application row from the database.

    Returns:
        Dict: The camelCase-converted application, with 'history' and
            'rounds' attached as additional keys.
    """
    conversion = utility_functions.to_camel_case_dict(app)
    conversion["history"] = database.get_application_logs(app["id"])
    conversion["round"] = database.get_interview_rounds(app["id"])
    return conversion


def import_single_application(job: Dict) -> int:
    """Validates and imports one job application record, including its rounds.

    Args:
        job (Dict): One raw application record from the import file.

    Returns:
        int: The ID of the newly created application.

    Raises:
        ValidationError: If the application data fails schema validation.
        RuntimeError: If the database insert fails.
    """
    app_model = JobApplication(**job)
    app_values = tuple(app_model.model_dump().values())
    history = job.get("history", [])
    new_id = database.add_job_application(app_values, history)

    for round_data in job.get("round", []):
        database.add_interview_round(
            new_id,
            round_data["round_label"],
            round_data["round_date"],
            round_data.get("notes", ""),
        )
    return new_id


def process_application_imports(applications: List[Dict]) -> Tuple[int, int]:
    """
    Validates and imports a list of raw dictionaries into the database.

    Each record is process individually. Most failures are considered failured
    imports by the system and will counted as such rather than imported.

    This function does not raise anay errors despite using them.

    Args:
     applications (List[Dict]): A list of dictonaries containing job applications.

    Returns:
     Tuple[int, int]: The first int is the number of passed imports and the second number is the number of failed imports.
    """
    imported_count, failed_count = 0, 0

    for job in applications:
        try:
            import_single_application(job)
            imported_count += 1
        except ValidationError:
            failed_count += 1
        except sqlite3.Error as error:
            raise sqlite3.Error(f"Database import failed: {error}")

    return imported_count, failed_count
