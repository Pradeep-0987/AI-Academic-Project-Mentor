import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project


def create_project(
    db: Session,
    student_id: uuid.UUID,
    title: str,
    description: str,
    domain: str | None = None,
    department: str | None = None,
    technology_stack: str | None = None,
    duration_weeks: int = 8,
    team_size: int | None = None,
    guide_name: str | None = None,
) -> Project:
    project = Project(
        student_id=student_id,
        title=title,
        description=description,
        domain=domain,
        department=department,
        technology_stack=technology_stack,
        duration_weeks=duration_weeks,
        team_size=team_size,
        guide_name=guide_name,
    )
    db.add(project)
    db.flush()
    return project


def list_by_student(db: Session, student_id: uuid.UUID) -> list[Project]:
    stmt = (
        select(Project)
        .where(Project.student_id == student_id)
        .order_by(Project.created_at.desc())
    )
    return list(db.scalars(stmt).all())