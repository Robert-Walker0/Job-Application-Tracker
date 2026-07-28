from fastapi import APIRouter, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse
from utility_functions import to_camel_case_dict
from models import JobApplication, JobApplicationUpdate, InterviewRound
import json
import database
import services

router = APIRouter()


@router.get("/")
def root() -> JSONResponse:
    """Gets the root REST API of the application.

    Returns:
        JSONResponse: Status 200 confirming the API is running, with a
            short message describing what the API is.
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
    """Gets all job applications.

    Returns:
        list: All applications, camelCase-converted. Empty list if none exist.
    """
    try:
        applications = database.get_all_job_applications()
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return [to_camel_case_dict(app) for app in applications]


@router.get("/applications/export/json")
def export_applications_json(filename: str = "job_applications") -> JSONResponse:
    """Exports all job applications as a downloadable JSON file.

    Args:
        filename (str): The filename to use for the downloaded file,
            without extension. Defaults to "job_applications".

    Returns:
        JSONResponse: The applications as a JSON list, with headers set to
            trigger a browser download.

    Raises:
        HTTPException 404: If there are no applications to export.
    """
    applications = database.get_all_job_applications()

    if not applications:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No job applications found to export.",
        )

    export_data = [services.build_export_record(app) for app in applications]

    return JSONResponse(
        content=export_data,
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}.json"'},
    )


@router.post("/applications/import/json")
async def import_applications_json(file: UploadFile = File(...)) -> JSONResponse:
    """Imports job applications from an uploaded JSON file.

    Bad or malformed individual records are skipped and counted as failed
    rather than aborting the whole import — see
    services.process_application_import.

    Args:
        file (UploadFile): The uploaded .json file containing a list of
            application records.

    Returns:
        JSONResponse: Status 201 with a summary of how many records were
            imported successfully versus failed.

    Raises:
        HTTPException 400: If the file isn't a .json file, isn't valid
            JSON, or isn't structured as a list.
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

    imported_count, failed_count = services.process_application_imports(
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
    """Creates a new job application.

    Args:
        application (JobApplication): The application data to create.

    Returns:
        JSONResponse: Status 201 with a confirmation message and the new
            application's ID.

    Raises:
        HTTPException 500: If the application fails to be created.
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
    """Creates a new interview round for an application.

    Args:
        application_id (int): The ID of the application this round belongs to.
        round_data (InterviewRound): The round's label, date, and optional notes.

    Returns:
        JSONResponse: Status 201 with a confirmation message and the new
            round's ID.

    Raises:
        HTTPException 500: If the round fails to be created.
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
    """Fetches all interview rounds for an application.

    Args:
        application_id (int): The ID of the application whose rounds to fetch.

    Returns:
        list: The application's interview rounds, camelCase-converted.

    Raises:
        HTTPException 404: If the application does not exist.
        HTTPException 500: If the rounds fail to be fetched.
    """
    try:
        rounds = database.get_interview_rounds(application_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )
    return [to_camel_case_dict(r) for r in rounds]


@router.get("/applications/{application_id}/history")
def get_application_history(application_id: int) -> list:
    """Fetches the change history for an application.

    Args:
        application_id (int): The ID of the application whose history to fetch.

    Returns:
        list: The application's log entries.

    Raises:
        HTTPException 404: If the application does not exist.
        HTTPException 500: If the history fails to be fetched.
    """
    try:
        logs = database.get_application_logs(application_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except RuntimeError as error:
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
        application (JobApplicationUpdate): The fields to update; unset
            fields are excluded and left unchanged.

    Returns:
        dict: The updated application, camelCase-converted.

    Raises:
        HTTPException 400: If no fields were provided to update.
        HTTPException 404: If the application does not exist.
        HTTPException 500: If the update fails.
    """
    updated_fields = application.model_dump(exclude_none=True)

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


@router.delete("/applications/all")
def delete_all_job_applications():
    try:
        deleted_count = database.delete_all_job_applications()
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "All applications deleted successfully.",
            "count": deleted_count,
        },
    )


@router.delete("/applications/{application_id}")
def delete_job_application_by_id(application_id: int) -> JSONResponse:
    try:
        deleted_id = database.delete_job_application_by_id(application_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Application deleted successfully.", "id": deleted_id},
    )
