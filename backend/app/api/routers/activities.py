from fastapi import APIRouter, Request, Response, status

from app.api.errors import (
    ACTIVITY_NAME_TAKEN_RESPONSE,
    ACTIVITY_NOT_FOUND_RESPONSE,
    INTERNAL_ERROR_RESPONSE,
    PROJECT_NOT_FOUND_RESPONSE,
    VALIDATION_ERROR_RESPONSE,
)
from app.api.headers import LOCATION_HEADER
from app.api.schemas.activities import ActivityRequest, ActivityResponse
from app.api.schemas.common import ActivityId, ProjectId
from app.db.session import DatabaseSession
from app.services import activity_service

router = APIRouter(
    prefix="/projects/{project_id}/activities",
    tags=["activities"],
    responses=INTERNAL_ERROR_RESPONSE,
)


@router.get(
    "",
    summary="List a project's activities",
    description="Activities of the project with their EVM indicators, ordered by id.",
    response_description="The project's activities with their indicators",
    responses=PROJECT_NOT_FOUND_RESPONSE | VALIDATION_ERROR_RESPONSE,
)
def list_activities(project_id: ProjectId, session: DatabaseSession) -> list[ActivityResponse]:
    return [
        ActivityResponse.from_result(result)
        for result in activity_service.list_activities(session, project_id)
    ]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create an activity",
    description="Adds an activity to the project and returns it with its EVM indicators. "
    "The Location header points to the new activity.",
    response_description="The created activity with its indicators",
    responses=PROJECT_NOT_FOUND_RESPONSE | ACTIVITY_NAME_TAKEN_RESPONSE | VALIDATION_ERROR_RESPONSE,
)
def create_activity(
    project_id: ProjectId,
    payload: ActivityRequest,
    request: Request,
    response: Response,
    session: DatabaseSession,
) -> ActivityResponse:
    result = activity_service.create_activity(session, project_id, payload.to_input())
    response.headers[LOCATION_HEADER] = str(
        request.url_for("get_activity", project_id=project_id, activity_id=result.record.id)
    )
    return ActivityResponse.from_result(result)


@router.get(
    "/{activity_id}",
    summary="Get an activity",
    description="One activity of the project with its EVM indicators.",
    response_description="The activity with its indicators",
    responses=ACTIVITY_NOT_FOUND_RESPONSE | VALIDATION_ERROR_RESPONSE,
)
def get_activity(
    project_id: ProjectId, activity_id: ActivityId, session: DatabaseSession
) -> ActivityResponse:
    return ActivityResponse.from_result(
        activity_service.get_activity(session, project_id, activity_id)
    )


@router.put(
    "/{activity_id}",
    summary="Replace an activity's data",
    description="Replaces every field of the activity; indicators are recalculated.",
    response_description="The updated activity with its recalculated indicators",
    responses=ACTIVITY_NOT_FOUND_RESPONSE
    | ACTIVITY_NAME_TAKEN_RESPONSE
    | VALIDATION_ERROR_RESPONSE,
)
def update_activity(
    project_id: ProjectId,
    activity_id: ActivityId,
    payload: ActivityRequest,
    session: DatabaseSession,
) -> ActivityResponse:
    result = activity_service.update_activity(session, project_id, activity_id, payload.to_input())
    return ActivityResponse.from_result(result)


@router.delete(
    "/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an activity",
    description="Deletes the activity; the project's consolidation changes accordingly.",
    response_description="The activity was deleted",
    responses=ACTIVITY_NOT_FOUND_RESPONSE | VALIDATION_ERROR_RESPONSE,
)
def delete_activity(
    project_id: ProjectId, activity_id: ActivityId, session: DatabaseSession
) -> None:
    activity_service.delete_activity(session, project_id, activity_id)
