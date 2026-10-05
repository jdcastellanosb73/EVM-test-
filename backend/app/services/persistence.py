from collections.abc import Mapping

from psycopg.errors import UniqueViolation
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import ActivityRecord, ProjectRecord
from app.services.errors import ConflictError, ErrorCode, NotFoundError


def find_project(session: Session, project_id: int) -> ProjectRecord:
    project = session.get(ProjectRecord, project_id)
    if project is None:
        raise NotFoundError(ErrorCode.PROJECT_NOT_FOUND, f"Project {project_id} not found")
    return project


def find_activity(session: Session, project_id: int, activity_id: int) -> ActivityRecord:
    find_project(session, project_id)
    activity = session.scalar(
        select(ActivityRecord).where(
            ActivityRecord.id == activity_id, ActivityRecord.project_id == project_id
        )
    )
    if activity is None:
        raise NotFoundError(
            ErrorCode.ACTIVITY_NOT_FOUND,
            f"Activity {activity_id} not found in project {project_id}",
        )
    return activity


def commit_or_raise_conflict(
    session: Session, conflicts_by_constraint: Mapping[str, ConflictError]
) -> None:
    """Commit, translating a unique-constraint violation into its business conflict.

    Relying on the database constraint (instead of checking first) is race-free.
    """
    try:
        session.commit()
    except IntegrityError as error:
        session.rollback()
        conflict = conflicts_by_constraint.get(_violated_unique_constraint(error))
        if conflict is None:
            raise
        raise conflict from error


def _violated_unique_constraint(error: IntegrityError) -> str:
    if isinstance(error.orig, UniqueViolation):
        return error.orig.diag.constraint_name or ""
    return ""
