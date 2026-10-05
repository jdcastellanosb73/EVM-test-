from decimal import Decimal

import pytest
from sqlalchemy import Connection
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import ActivityRecord, ProjectRecord
from app.services.persistence import commit_or_raise_conflict


def test_integrity_errors_that_are_not_name_conflicts_are_not_hidden(
    database_connection: Connection,
) -> None:
    with Session(bind=database_connection, join_transaction_mode="create_savepoint") as session:
        project = ProjectRecord(name="Proyecto")
        session.add(project)
        session.flush()
        session.add(
            ActivityRecord(
                project_id=project.id,
                name="BAC inválido",
                budget_at_completion=Decimal(0),
                planned_percent=Decimal(0),
                actual_percent=Decimal(0),
                actual_cost=Decimal(0),
            )
        )

        with pytest.raises(IntegrityError, match="ck_activities_bac_positive"):
            commit_or_raise_conflict(session, {})
