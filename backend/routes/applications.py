from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from database import add_job_application, get_all_job_applications, get_job_application_by_id
from utility_functions import convert_keys
from models import JobApplication

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

@router.get("/applications/export/csv")
def export_applications_csv():
    pass


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
