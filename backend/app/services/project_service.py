import logging
import uuid
from copy import deepcopy
from datetime import date, timedelta
from pathlib import Path
import sys
from sqlalchemy.orm import Session

# Ensure project root is in sys.path so ai_engine is accessible
_root = str(Path(__file__).resolve().parent.parent.parent.parent)
if _root not in sys.path:
    sys.path.insert(0, _root)

from ai_engine.workflows.blueprint_graph import generate_blueprint
from app.models.project import Project
from app.models.user import User
from app.repositories import blueprint_repository, project_repository, student_repository
from app.schemas.project import BlueprintPreviewRequest, ProjectCreate

logger = logging.getLogger(__name__)


class BlueprintGenerationError(RuntimeError):
    pass


def _with_milestone_tracking(
    blueprint: dict,
    duration_weeks: int,
    start_date: date | None = None,
) -> dict:
    planning = blueprint.get("planning", {})
    milestones = planning.get("weekly_milestones", [])
    start_date = start_date or date.today()
    for milestone in milestones:
        week = milestone.get("week_number", 1)
        milestone.setdefault("status", "pending")
        milestone.setdefault("progress", 0)
        milestone.setdefault(
            "expected_completion_date",
            (start_date + timedelta(weeks=week - 1, days=6)).isoformat(),
        )
    planning["total_duration_weeks"] = duration_weeks
    planning["weekly_milestones"] = milestones
    blueprint["planning"] = planning
    return blueprint


def create_project(db: Session, user: User, data: ProjectCreate) -> Project:
    try:
        student_skills = student_repository.get_skills(db, user.id)
        skills_list = [s.skill_name for s in student_skills]
        db.rollback()

        details = [
            data.title,
            data.description,
            f"Domain: {data.domain}" if data.domain else "",
            f"Department: {data.department}" if data.department else "",
            f"Technology stack: {data.technology_stack}" if data.technology_stack else "",
        ]
        full_idea = ". ".join(part for part in details if part).strip()
        try:
            bp_result = generate_blueprint(
                project_idea=full_idea,
                duration_weeks=data.duration_weeks,
                team_size=data.team_size,
                skills=skills_list,
            )
        except Exception as exc:
            logger.exception("AI blueprint generation failed for a new project")
            raise BlueprintGenerationError(
                "NEXTSTEP AI could not generate a blueprint. Please try again; no project was saved."
            ) from exc

        project = project_repository.create_project(
            db,
            student_id=user.id,
            title=data.title,
            description=data.description,
            domain=data.domain,
            department=data.department,
            technology_stack=data.technology_stack,
            duration_weeks=data.duration_weeks,
            team_size=data.team_size,
            guide_name=data.guide_name,
        )
        bp_result = _with_milestone_tracking(
            bp_result, data.duration_weeks, project.created_at.date()
        )
        blueprint_repository.upsert_blueprint(db, project.id, bp_result)
        db.commit()
        db.refresh(project)
        logger.info("Project and AI blueprint saved for project %s", project.id)
        return project
    except Exception:
        db.rollback()
        raise


def list_projects(db: Session, user: User) -> list[Project]:
    projects = project_repository.list_by_student(db, user.id)
    for project in projects:
        blueprint = blueprint_repository.get_by_project_id(db, project.id)
        milestones = (
            _with_milestone_tracking(
                {"planning": blueprint.planning},
                project.duration_weeks,
                project.created_at.date(),
            )["planning"]["weekly_milestones"]
            if blueprint else []
        )
        project.total_milestones = len(milestones)
        project.milestones_completed = sum(m.get("status") == "completed" for m in milestones)
        project.progress = (
            round(project.milestones_completed * 100 / project.total_milestones)
            if project.total_milestones else 0
        )
        pending = [m for m in milestones if m.get("status") != "completed"]
        project.delayed_milestones = sum(
            bool(m.get("expected_completion_date"))
            and m["expected_completion_date"] < date.today().isoformat()
            for m in pending
        )
        next_milestone = min(
            (m for m in pending if m.get("expected_completion_date")),
            key=lambda m: m["expected_completion_date"],
            default=None,
        )
        project.next_deadline = next_milestone.get("expected_completion_date") if next_milestone else None
        project.next_milestone = next_milestone.get("milestone_title") if next_milestone else None
    return projects


def get_project_blueprint(db: Session, user: User, project_id: uuid.UUID) -> dict | None:
    # Ensure project belongs to current student
    projects = project_repository.list_by_student(db, user.id)
    target = next((p for p in projects if p.id == project_id), None)
    if not target:
        return None

    bp = blueprint_repository.get_by_project_id(db, project_id)
    if not bp:
        return None

    result = {
        "project_id": bp.project_id,
        "feasibility": bp.feasibility,
        "scope": bp.scope,
        "technology": bp.technology,
        "planning": _with_milestone_tracking(
            {"planning": bp.planning}, target.duration_weeks, target.created_at.date()
        )["planning"],
        "risk": bp.risk,
        "quality_report": bp.quality_report,
        "created_at": bp.created_at,
    }
    return result


def trigger_project_blueprint(
    db: Session,
    user: User,
    project_id: uuid.UUID,
    duration_weeks: int | None = None,
    team_size: int | None = None,
) -> dict | None:
    projects = project_repository.list_by_student(db, user.id)
    project = next((p for p in projects if p.id == project_id), None)
    if not project:
        return None

    student_skills = student_repository.get_skills(db, user.id)
    skills_list = [s.skill_name for s in student_skills]

    full_idea = ". ".join(part for part in (
        project.title,
        project.description,
        f"Domain: {project.domain}" if project.domain else "",
        f"Department: {project.department}" if project.department else "",
        f"Technology stack: {project.technology_stack}" if project.technology_stack else "",
    ) if part).strip()
    requested_duration = duration_weeks or project.duration_weeks
    requested_team_size = team_size or project.team_size
    try:
        bp_result = generate_blueprint(
            project_idea=full_idea,
            duration_weeks=requested_duration,
            team_size=requested_team_size,
            skills=skills_list,
        )
    except Exception as exc:
        logger.exception("AI blueprint regeneration failed for project %s", project_id)
        raise BlueprintGenerationError(
            "NEXTSTEP AI could not regenerate this blueprint. Please try again."
        ) from exc

    try:
        bp_result = _with_milestone_tracking(bp_result, requested_duration)
        project.duration_weeks = requested_duration
        if team_size is not None:
            project.team_size = team_size
        bp = blueprint_repository.upsert_blueprint(db, project.id, bp_result)
        db.commit()
        db.refresh(bp)
    except Exception:
        db.rollback()
        raise

    result = {
        "project_id": bp.project_id,
        "feasibility": bp.feasibility,
        "scope": bp.scope,
        "technology": bp.technology,
        "planning": bp.planning,
        "risk": bp.risk,
        "quality_report": bp.quality_report,
        "created_at": bp.created_at,
    }
    return result


def preview_blueprint(data: BlueprintPreviewRequest) -> dict:
    blueprint = generate_blueprint(
        project_idea=data.idea,
        duration_weeks=data.duration_weeks,
        team_size=data.team_size,
        skills=data.skills,
    )
    return _with_milestone_tracking(blueprint, data.duration_weeks)


def update_milestone_status(
    db: Session,
    user: User,
    project_id: uuid.UUID,
    week_number: int,
    milestone_status: str,
) -> dict | None:
    project = next(
        (p for p in project_repository.list_by_student(db, user.id) if p.id == project_id),
        None,
    )
    if project is None:
        return None
    blueprint = blueprint_repository.get_by_project_id(db, project_id)
    if blueprint is None:
        return None
    planning = _with_milestone_tracking(
        {"planning": deepcopy(blueprint.planning)},
        project.duration_weeks,
        project.created_at.date(),
    )["planning"]
    milestone = next(
        (m for m in planning["weekly_milestones"] if m.get("week_number") == week_number),
        None,
    )
    if milestone is None:
        return None
    milestone["status"] = milestone_status
    milestone["progress"] = 100 if milestone_status == "completed" else 0
    blueprint.planning = planning
    all_milestones = planning["weekly_milestones"]
    project.status = (
        "completed"
        if all_milestones and all(m.get("status") == "completed" for m in all_milestones)
        else "submitted"
    )
    db.commit()
    db.refresh(blueprint)
    return get_project_blueprint(db, user, project_id)