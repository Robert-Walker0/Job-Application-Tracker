from pydantic import ValidationError
from models import JobApplication
from typing import List, Dict, Tuple
import sqlite3
import database


def process_application_import(applications: List[Dict]) -> Tuple[int, int]:
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
            app_model = JobApplication(**job)
            app_values = tuple(app_model.model_dump().values())
            history = job.get("history", [])
            database.add_job_application(app_values, history)
            imported_count += 1
        except ValidationError:
            failed_count += 1
        except sqlite3.Error as error:
            raise sqlite3.Error(f"Database import failed: {error}")

    return imported_count, failed_count
