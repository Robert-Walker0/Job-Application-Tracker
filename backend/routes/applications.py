from fastapi import APIRouter, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from database import add_job_application, get_all_job_applications, get_job_application_by_id
from utility_functions import convert_keys
from models import JobApplication
import json

router = APIRouter()

@router.get("/")
def root() -> dict:
    return {"message": "Job Application Tracker API"}


@router.get("/applications/{application_id}")
def get_application(application_id: int) -> dict:
    try:
        return get_job_application_by_id(application_id)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Application {application_id} not found")

@router.get("/applications")
def get_applications() -> list:
    applications = get_all_job_applications()
    return [convert_keys(app) for app in applications]


@router.get("/applications/export/json")
def export_applications_json(filename: str = "job_applications"):
    try:
        job_applications = get_all_job_applications()
        if not job_applications: raise ValueError("The database is empty.")
        list_of_job_applications = [convert_keys(app) for app in job_applications]
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
async def import_applications_json(file: UploadFile = File(...)):
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

    imported_count = 0
    failed_count = 0

    for application in applications:
        try:
            add_job_application((
                application.get("company"),
                application.get("jobTitle"),
                application.get("dateApplied"),
                application.get("platform"),
                application.get("link"),
                application.get("payType"),
                application.get("payAmount"),
                application.get("notes"),
                application.get("status"),
                application.get("lastHeardFrom")
            ))
            imported_count += 1
        except RuntimeError:
            failed_count += 1

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": f"Import complete. {imported_count} imported, {failed_count} failed."
        }
    )


@router.post("/applications")
def create_application(application: JobApplication) -> dict:
    try:
        add_job_application((
                application.company,
                application.job_title,
                application.date_applied,
                application.platform,
                application.link,
                application.pay_type,
                application.pay_amount,
                application.notes,
                application.status,
                application.last_heard_from
            ))      
    except RuntimeError as error:
        raise HTTPException(status_code=500, detail=str(error))
    
    return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Application has been added successfully."}
        )
