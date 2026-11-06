import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.blueprint import ProjectBlueprint


def get_by_project_id(db: Session, project_id: uuid.UUID) -> ProjectBlueprint | None:
    stmt = select(ProjectBlueprint).where(ProjectBlueprint.project_id == project_id)
    return db.scalar(stmt)


def upsert_blueprint(db: Session, project_id: uuid.UUID, blueprint_data: dict) -> ProjectBlueprint:
    existing = get_by_project_id(db, project_id)
    if existing:
        existing.feasibility = blueprint_data.get("feasibility", {})
        existing.scope = blueprint_data.get("scope", {})
        existing.technology = blueprint_data.get("technology", {})
        existing.planning = blueprint_data.get("planning", {})
        existing.risk = blueprint_data.get("risk", {})
        existing.quality_report = blueprint_data.get("quality_report", {})
        db.flush()
        return existing

    bp = ProjectBlueprint(
        project_id=project_id,
        feasibility=blueprint_data.get("feasibility", {}),
        scope=blueprint_data.get("scope", {}),
        technology=blueprint_data.get("technology", {}),
        planning=blueprint_data.get("planning", {}),
        risk=blueprint_data.get("risk", {}),
        quality_report=blueprint_data.get("quality_report", {}),
    )
    db.add(bp)
    db.flush()
    return bp
