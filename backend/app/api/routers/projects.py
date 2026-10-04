from fastapi import APIRouter, Request, Response, status

from app.api.errors import (
    PROJECT_NAME_TAKEN_RESPONSE,
    PROJECT_NOT_FOUND_RESPONSE,
    VALIDATION_ERROR_RESPONSE,
)
from app.api.schemas.common import ProjectId
from app.api.schemas.projects import ProjectRequest, ProjectResponse, ProjectSummaryResponse
from app.db.session import DatabaseSession
from app.services import project_service

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get(
    "",
    summary="List projects",
    description="Every project with its consolidated EVM indicators, ordered by id.",
)
def list_projects(session: DatabaseSession) -> list[ProjectSummaryResponse]:
    return [
        ProjectSummaryResponse.from_result(result)
        for result in project_service.list_projects(session)
    ]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create a project",
    description="Creates an empty project. Its indicators are 0 and its indices null "
    "until activities are added. The Location header points to the new project.",
    responses=PROJECT_NAME_TAKEN_RESPONSE | VALIDATION_ERROR_RESPONSE,
)
def create_project(
    payload: ProjectRequest, request: Request, response: Response, session: DatabaseSession
) -> ProjectResponse:
    result = project_service.create_project(session, payload.to_input())
    response.headers["Location"] = str(request.url_for("get_project", project_id=result.record.id))
    return ProjectResponse.from_result(result)


@router.get(
    "/{project_id}",
    summary="Get a project with its activities",
    description="Project, its activities with their indicators, and the consolidated "
    "indicators: everything the dashboard needs in one call.",
    responses=PROJECT_NOT_FOUND_RESPONSE | VALIDATION_ERROR_RESPONSE,
)
def get_project(project_id: ProjectId, session: DatabaseSession) -> ProjectResponse:
    return ProjectResponse.from_result(project_service.get_project(session, project_id))


@router.put(
    "/{project_id}",
    summary="Replace a project's data",
    description="Replaces name, description and cutoff date. Activities are not touched.",
    responses=PROJECT_NOT_FOUND_RESPONSE | PROJECT_NAME_TAKEN_RESPONSE | VALIDATION_ERROR_RESPONSE,
)
def update_project(
    project_id: ProjectId, payload: ProjectRequest, session: DatabaseSession
) -> ProjectResponse:
    result = project_service.update_project(session, project_id, payload.to_input())
    return ProjectResponse.from_result(result)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project",
    description="Deletes the project and, in cascade, all of its activities.",
    responses=PROJECT_NOT_FOUND_RESPONSE | VALIDATION_ERROR_RESPONSE,
)
def delete_project(project_id: ProjectId, session: DatabaseSession) -> None:
    project_service.delete_project(session, project_id)
