from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.db.models import PROJECT_NAME_UNIQUE_CONSTRAINT, ProjectRecord
from app.services.errors import ConflictError, ErrorCode
from app.services.persistence import commit_or_raise_conflict, find_project
from app.services.results import ProjectInput, ProjectResult, build_project_result


def list_projects(session: Session) -> list[ProjectResult]:
    projects = session.scalars(
        select(ProjectRecord)
        .options(selectinload(ProjectRecord.activities))
        .order_by(ProjectRecord.id)
    )
    return [build_project_result(project) for project in projects]


def get_project(session: Session, project_id: int) -> ProjectResult:
    return build_project_result(find_project(session, project_id))


def create_project(session: Session, data: ProjectInput) -> ProjectResult:
    project = ProjectRecord()
    _apply(project, data)
    session.add(project)
    _save(session, project, data)
    return build_project_result(project)


def update_project(session: Session, project_id: int, data: ProjectInput) -> ProjectResult:
    project = find_project(session, project_id)
    _apply(project, data)
    _save(session, project, data)
    return build_project_result(project)


def delete_project(session: Session, project_id: int) -> None:
    """Activities are removed by the database (ON DELETE CASCADE)."""
    session.delete(find_project(session, project_id))
    session.commit()


def _apply(project: ProjectRecord, data: ProjectInput) -> None:
    project.name = data.name
    project.description = data.description
    project.cutoff_date = data.cutoff_date


def _save(session: Session, project: ProjectRecord, data: ProjectInput) -> None:
    name_taken = ConflictError(
        ErrorCode.PROJECT_NAME_TAKEN, f"A project named '{data.name}' already exists"
    )
    commit_or_raise_conflict(session, {PROJECT_NAME_UNIQUE_CONSTRAINT: name_taken})
    session.refresh(project)
