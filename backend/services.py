from pydantic import ValidationError
from models import JobApplication
from typing import List, Dict, Tuple
import sqlite3
import database


def process_application_import(application_data: List[Dict]) -> Tuple[int, int]:
    """
    Validates and imports a list of raw dictionaries into the database
    Returns (imported_count, failed_count).
    """
    imported_count = 0
    failed_count = 0

    for raw_app in application_data:
        try:
            app_model = JobApplication(**raw_app)
            app_values = tuple(app_model.model_dump().values())
            history = raw_app.get("history", [])
            database.add_job_application(app_values, history)
            imported_count += 1
        except (ValidationError, sqlite3.Error, RuntimeError):
            failed_count += 1

    return imported_count, failed_count
