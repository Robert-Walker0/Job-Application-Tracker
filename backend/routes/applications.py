from fastapi import APIRouter, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from utility_functions import to_camel_case_dict
from models import JobApplication, JobApplicationUpdate, InterviewRound
import json, database, services

router = APIRouter()


@router.get("/")
def root() -> JSONResponse:
    """Gets the root REST API of the application.

    Returns:
        JSONResponse: The application status code of 200 to signal that
        root of the application is working correctly. Along with content
        about what the API is about.
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Job Application Tracker API"},
    )


@router.get("/applications/{application_id}")
def get_application(application_id: int) -> dict:
    try:
        return database.get_job_application_by_id(application_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application {application_id} not found",
        )


@router.get("/applications")
def get_applications() -> list:
    """Gets all of the applications and converts them into a list.

    Returns:
        list: A list of all the applications.
    """
    applications = database.get_all_job_applications()
    return [to_camel_case_dict(app) for app in applications]


@router.get("/applications/export/json")
def export_applications_json(filename: str = "job_applications"):
    """Exports all of the current job applications from the database.

    Collects all the current job applications from the database and
    converts them into a list JSON format for downloading.

    Args:
        filename (str): The filename that will be used for the user when downloading the file.

    Returns:
        JSONResponse: A JSON response of the job applications in a list along with the processing
        data on how to download it, notes on json file type and how the content is being received
        by the browser.

    Raises:
        HTTPException 404: If no job applications are available to be exported to download.
    """
    applications = database.get_all_job_applications()

    if not applications:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No job applications found to export.",
        )

    export_data = []
    for app in applications:
        converted = to_camel_case_dict(app)
        converted["history"] = database.get_application_logs(app["id"])
        export_data.append(converted)

    return JSONResponse(
        content=export_data,
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}.json"'},
    )


@router.post("/applications/import/json")
async def import_applications_json(file: UploadFile = File(...)):
    """Imports job application only in JSON file format.

    Ensures that any files are not json files, invalid json, or
    have invalid structure are rejected imports.

    Args:
        file (UploadFile): The file being processed for the import. Defaults to a File.

    Returns:
        JSONResponse: A successful status code 201 for posting one or multiple
        job applications onto the server. The extra data included the message
        goes over how many success imports were completed and how many failed.

    Raises:
        HTTPException 400: If the file received is not JSON format, invalid JSON file, or is not in list format of applications.

    """
    if not file.filename.endswith(".json"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only .json files are accepted.",
        )

    try:
        contents = await file.read()
        applications_data = json.loads(contents)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON file. Please upload a valid exported file.",
        )

    if not isinstance(applications_data, list):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file structure. Expected a list of applications.",
        )

    imported_count, failed_count = services.process_application_import(
        applications_data
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": f"Import complete. {imported_count} imported, {failed_count} failed."
        },
    )


@router.post("/applications")
def create_application(application: JobApplication) -> JSONResponse:
    """Creates a job application

    Args:
        application (JobApplication): The job application form with its data.

    Returns:
        JSONResponse: A successful status code of 201 for creating a
        new job application on the server. In the response as extra data is a message
        stating that the job application was created successfully along with
        its new id.

    Raises:
        HTTPException 500: If the server had an error that prevented the creation of a job application.
    """
    try:
        new_id = database.add_job_application(tuple(application.model_dump().values()))
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Application has been added successfully.", "id": new_id},
    )


@router.post("/applications/{application_id}/interview-rounds")
def create_interview_round(
    application_id: int, round_data: InterviewRound
) -> JSONResponse:
    """Creates an interview round.

    Args:
        application_id (int):
        round_data (InterviewRound):

    Returns:
        JSONResponse: A successful status code of 201 for creating a
        new interview round on the server. In the response as extra data is a message
        stating that the interview round was created successfully along with
        its new id.

    Raises:
        HTTPException 500: If there was a server error with creating a interview round.
    """
    try:
        new_id = database.add_interview_round(
            application_id,
            round_data.round_label,
            round_data.round_date,
            round_data.notes,
        )
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Interview round added successfully.", "id": new_id},
    )


@router.get("/applications/{application_id}/interview-rounds")
def get_interview_rounds(application_id: int) -> list:
    """Fetches the interview rounds for a specific job application.

    Args:
        application_id (int): The job application id

    Returns:
        list: Returns a list of rounds for that job application.

    Raises:
        HTTPException 500: If the application or rounds couldn't be fetched from the server.
    """
    try:
        rounds = database.get_interview_rounds(application_id)
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return [to_camel_case_dict(r) for r in rounds]


@router.get("/applications/{application_id}/history")
def get_application_history(application_id: int) -> list:
    """Gathers the history an existing job application.

    Args:
        application_id (int): The job application id

    Returns:
        list: A list of the logs messaages for that job application.

    Raises:
        HTTPException 500: If the application was failed to be fetched from the server.
    """
    try:
        logs = database.get_application_logs(application_id)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch application history: {str(error)}",
        )
    return logs


@router.put("/applications/{application_id}")
def update_job_application_by_id(
    application_id: int, application: JobApplicationUpdate
) -> dict:
    """Updates an existing job application.

    Args:
        application_id (int): The ID of the application to update.
        application (JobApplicationUpdate): The Job Application Update Model to use to update.

    Returns:
        dict: The updated application data.

    Raises:
        HTTPException 404: If application not found.
        HTTPException 500: If database update fails.
    """
    updated_fields = {
        key: value for key, value in application.model_dump(exclude_none=True).items()
    }

    if not updated_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided to update.",
        )

    try:
        updated = database.update_job_application(application_id, updated_fields)
        return to_camel_case_dict(updated)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Application {application_id} not found.",
        )
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
