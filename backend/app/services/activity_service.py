from sqlalchemy.orm import Session

from app.db.models import ACTIVITY_NAME_UNIQUE_CONSTRAINT, ActivityRecord
from app.services.errors import ConflictError, ErrorCode
from app.services.persistence import commit_or_raise_conflict, find_activity, find_project
from app.services.results import ActivityInput, ActivityResult, build_activity_result


def list_activities(session: Session, project_id: int) -> list[ActivityResult]:
    project = find_project(session, project_id)
    return [build_activity_result(activity) for activity in project.activities]


def get_activity(session: Session, project_id: int, activity_id: int) -> ActivityResult:
    return build_activity_result(find_activity(session, project_id, activity_id))


def create_activity(session: Session, project_id: int, data: ActivityInput) -> ActivityResult:
    find_project(session, project_id)
    activity = ActivityRecord(project_id=project_id)
    _apply(activity, data)
    session.add(activity)
    _save(session, activity, data)
    return build_activity_result(activity)


def update_activity(
    session: Session, project_id: int, activity_id: int, data: ActivityInput
) -> ActivityResult:
    activity = find_activity(session, project_id, activity_id)
    _apply(activity, data)
    _save(session, activity, data)
    return build_activity_result(activity)


def delete_activity(session: Session, project_id: int, activity_id: int) -> None:
    session.delete(find_activity(session, project_id, activity_id))
    session.commit()


def _apply(activity: ActivityRecord, data: ActivityInput) -> None:
    activity.name = data.name
    activity.budget_at_completion = data.progress.budget_at_completion
    activity.planned_percent = data.progress.planned_percent
    activity.actual_percent = data.progress.actual_percent
    activity.actual_cost = data.progress.actual_cost


def _save(session: Session, activity: ActivityRecord, data: ActivityInput) -> None:
    name_taken = ConflictError(
        ErrorCode.ACTIVITY_NAME_TAKEN,
        f"An activity named '{data.name}' already exists in project {activity.project_id}",
    )
    commit_or_raise_conflict(session, {ACTIVITY_NAME_UNIQUE_CONSTRAINT: name_taken})
    session.refresh(activity)
