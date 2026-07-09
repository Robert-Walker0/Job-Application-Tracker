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
