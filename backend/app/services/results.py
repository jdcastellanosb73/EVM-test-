from dataclasses import dataclass
from datetime import date

from app.db.models import ActivityRecord, ProjectRecord
from app.domain.evm import (
    ActivityProgress,
    EvmIndicators,
    calculate_activity_indicators,
    consolidate_project_indicators,
)


@dataclass(frozen=True, slots=True)
class ProjectInput:
    name: str
    description: str | None
    cutoff_date: date | None


@dataclass(frozen=True, slots=True)
class ActivityInput:
    name: str
    progress: ActivityProgress


@dataclass(frozen=True, slots=True)
class ActivityResult:
    record: ActivityRecord
    indicators: EvmIndicators


@dataclass(frozen=True, slots=True)
class ProjectResult:
    record: ProjectRecord
    activities: list[ActivityResult]
    indicators: EvmIndicators


def progress_of(activity: ActivityRecord) -> ActivityProgress:
    return ActivityProgress(
        budget_at_completion=activity.budget_at_completion,
        planned_percent=activity.planned_percent,
        actual_percent=activity.actual_percent,
        actual_cost=activity.actual_cost,
    )


def build_activity_result(activity: ActivityRecord) -> ActivityResult:
    """Indicators are computed on read from the stored inputs; they are never persisted."""
    return ActivityResult(
        record=activity, indicators=calculate_activity_indicators(progress_of(activity))
    )


def build_project_result(project: ProjectRecord) -> ProjectResult:
    return ProjectResult(
        record=project,
        activities=[build_activity_result(activity) for activity in project.activities],
        indicators=consolidate_project_indicators(
            progress_of(activity) for activity in project.activities
        ),
    )
