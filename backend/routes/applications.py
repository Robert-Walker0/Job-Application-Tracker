from fastapi import APIRouter, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from utility_functions import to_camel_case_dict
from models import JobApplication, JobApplicationUpdate
import json, database

router = APIRouter()

@router.get("/")
def root() -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Job Application Tracker API"}
    )

@router.get("/applications/{application_id}")
def get_application(application_id: int) -> dict:
    try:
        return database.get_job_application_by_id(application_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Application {application_id} not found"
        )

@router.get("/applications")
def get_applications() -> list:
    applications = database.get_all_job_applications()
    return [to_camel_case_dict(app) for app in applications]


@router.get("/applications/export/json")
def export_applications_json(filename: str = "job_applications") -> JSONResponse:
    try:
        job_applications = database.get_all_job_applications()
        if not job_applications: raise ValueError("The database is empty.")
        list_of_job_applications = [to_camel_case_dict(app) for app in job_applications]
        safe_filename = filename if filename.endswith(".json") else f"{filename}.json"

        return JSONResponse(
            content=list_of_job_applications,
            headers={
                "Content-Disposition": f"attachment; filename={safe_filename}"
            }
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No job applications found to export."
        )
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Export failed: {str(error)}"
        )

@router.post("/applications/import/json")
async def import_applications_json(file: UploadFile = File(...)) -> JSONResponse:
    if not file.filename.endswith(".json"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only .json files are accepted."
        )

    try:
        contents = await file.read()
        applications = json.loads(contents)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON file. Please upload a valid exported file."
        )

    if not isinstance(applications, list):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file structure. Expected a list of applications."
        )

    added_entries = 0
    errors_collected = 0
    required_keys = [field.alias if field.alias else name for name, field in JobApplication.model_fields.items()]

    for application in applications:
        try:
            app_tuple = tuple(application.get(key) for key in required_keys)
            database.add_job_application(app_tuple)
            added_entries += 1
        except RuntimeError:
            errors_collected += 1

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": f"Import complete. {added_entries} imported, {errors_collected} failed."
        }
    )


@router.post("/applications")
def create_application(application: JobApplication) -> JSONResponse:
    try:
        database.add_job_application(tuple(application.model_dump().values())) 
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(error)
        )
    
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Application has been added successfully."}
    )

@router.get("/applications/{application_id}/history")
def get_application_history(application_id: int) -> list:
    try:
        logs = database.get_application_logs(application_id)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch application history: {str(error)}"
        )
    return logs

@router.put("/applications/{application_id}")
def update_job_application_by_id(application_id: int, application: JobApplicationUpdate) -> dict:
    """Updates an existing job application.

    Args:
        application_id: The ID of the application to update.
        application: The fields to update.

    Returns:
        dict: The updated application data.

    Raises:
        HTTPException 404: If application not found.
        HTTPException 500: If database update fails.
    """
    updated_fields = {
        key: value 
        for key, value in application.model_dump(exclude_none=True).items()
    }

    if not updated_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided to update."
        )

    try:
        updated = database.update_job_application(application_id, updated_fields)
        return to_camel_case_dict(updated)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application {application_id} not found."
        )
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error)
        )