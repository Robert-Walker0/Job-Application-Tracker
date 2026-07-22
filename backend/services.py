from pydantic import ValidationError
from models import JobApplication
from typing import List, Dict, Tuple
import sqlite3
import database


def process_application_import(application_data: List[Dict]) -> Tuple[int, int]:
    """
    Validates and imports a list of raw dictionaries into the database.

    Each record is process individually. Most failures are considered failured
    imports by the system and will counted as such rather than imported.

    This function does not raise anay errors despite using them.

    Args:
     application_data (List[Dict]): A list of dictonaries containing job applications.

    Returns:
     Tuple[int, int]: The first int is the number of passed imports and the second number is the number of failed imports.
    """
    imported_count, failed_count = 0, 0

    for raw_app in application_data:
        try:
            app_model = JobApplication(**raw_app)
            app_values = tuple(app_model.model_dump().values())
            history = raw_app.get("history", [])
            database.add_job_application(app_values, history)
            imported_count += 1
        except Exception as e:
            failed_count += 1

    return imported_count, failed_count
