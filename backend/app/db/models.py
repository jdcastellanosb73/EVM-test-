"""ORM mapping of db/init/01_schema.sql, which remains the source of truth for the schema."""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    Date,
    DateTime,
    FetchedValue,
    ForeignKey,
    Identity,
    Index,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

NAME_MAX_LENGTH = 120
DESCRIPTION_MAX_LENGTH = 500
MONEY_PRECISION = 15
PERCENT_PRECISION = 5
DECIMAL_SCALE = 2

PROJECT_NAME_UNIQUE_CONSTRAINT = "uq_projects_name"
ACTIVITY_NAME_UNIQUE_CONSTRAINT = "uq_activities_project_name"
NAME_NOT_BLANK_RULE = "length(trim(name)) > 0"


class Base(DeclarativeBase):
    pass


class ProjectRecord(Base):
    __tablename__ = "projects"
    __table_args__ = (
        UniqueConstraint("name", name=PROJECT_NAME_UNIQUE_CONSTRAINT),
        CheckConstraint(NAME_NOT_BLANK_RULE, name="ck_projects_name_not_blank"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH))
    description: Mapped[str | None] = mapped_column(String(DESCRIPTION_MAX_LENGTH))
    cutoff_date: Mapped[date | None] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=FetchedValue()
    )

    activities: Mapped[list["ActivityRecord"]] = relationship(
        back_populates="project",
        order_by="ActivityRecord.id",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ActivityRecord(Base):
    __tablename__ = "activities"
    __table_args__ = (
        UniqueConstraint("project_id", "name", name=ACTIVITY_NAME_UNIQUE_CONSTRAINT),
        CheckConstraint(NAME_NOT_BLANK_RULE, name="ck_activities_name_not_blank"),
        CheckConstraint("budget_at_completion > 0", name="ck_activities_bac_positive"),
        CheckConstraint(
            "planned_percent BETWEEN 0 AND 100", name="ck_activities_planned_percent_range"
        ),
        CheckConstraint(
            "actual_percent BETWEEN 0 AND 100", name="ck_activities_actual_percent_range"
        ),
        CheckConstraint("actual_cost >= 0", name="ck_activities_actual_cost_non_negative"),
        Index("ix_activities_project_id", "project_id"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(always=True), primary_key=True)
    project_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("projects.id", ondelete="CASCADE", name="fk_activities_project")
    )
    name: Mapped[str] = mapped_column(String(NAME_MAX_LENGTH))
    budget_at_completion: Mapped[Decimal] = mapped_column(Numeric(MONEY_PRECISION, DECIMAL_SCALE))
    planned_percent: Mapped[Decimal] = mapped_column(Numeric(PERCENT_PRECISION, DECIMAL_SCALE))
    actual_percent: Mapped[Decimal] = mapped_column(Numeric(PERCENT_PRECISION, DECIMAL_SCALE))
    actual_cost: Mapped[Decimal] = mapped_column(Numeric(MONEY_PRECISION, DECIMAL_SCALE))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), server_onupdate=FetchedValue()
    )

    project: Mapped[ProjectRecord] = relationship(back_populates="activities")
