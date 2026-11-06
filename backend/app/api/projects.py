import logging
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.project import (
    BlueprintPreviewRequest,
    BlueprintResponse,
    MentorChatRequest,
    MilestoneStatusUpdate,
    ProjectCreate,
    ProjectListItem,
    ProjectResponse,
)
from app.services import project_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return project_service.create_project(db, current_user, data)
    except project_service.BlueprintGenerationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    except SQLAlchemyError as exc:
        logger.exception("Project creation failed while saving to the database")
        raise HTTPException(
            status_code=500,
            detail="The project could not be saved. Please try again; contact support if the problem continues.",
        ) from exc


@router.get("", response_model=list[ProjectListItem])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return project_service.list_projects(db, current_user)


@router.get("/{project_id}/blueprint", response_model=BlueprintResponse)
def get_project_blueprint(
    project_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    bp = project_service.get_project_blueprint(db, current_user, project_id)
    if not bp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blueprint not found for this project.",
        )
    return bp


@router.post("/{project_id}/blueprint", response_model=BlueprintResponse)
def generate_project_blueprint(
    project_id: uuid.UUID,
    duration_weeks: int | None = None,
    team_size: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        bp = project_service.trigger_project_blueprint(
            db, current_user, project_id, duration_weeks=duration_weeks, team_size=team_size
        )
    except project_service.BlueprintGenerationError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    if not bp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or not owned by student.",
        )
    return bp


@router.patch("/{project_id}/milestones/{week_number}", response_model=BlueprintResponse)
def update_milestone(
    project_id: uuid.UUID,
    week_number: int,
    data: MilestoneStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    blueprint = project_service.update_milestone_status(
        db, current_user, project_id, week_number, data.status
    )
    if not blueprint:
        raise HTTPException(status_code=404, detail="Project or milestone not found.")
    return blueprint


@router.post("/{project_id}/chat")
def chat_about_project(
    project_id: uuid.UUID,
    data: MentorChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = next(
        (p for p in project_service.list_projects(db, current_user) if p.id == project_id),
        None,
    )
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found.")
    blueprint = project_service.get_project_blueprint(db, current_user, project_id)
    if blueprint is None:
        raise HTTPException(status_code=404, detail="Blueprint not found for this project.")

    from ai_engine.mentor.chat_service import chat_with_mentor

    context = {
        "project": {
            "title": project.title,
            "description": project.description,
            "domain": project.domain,
            "department": project.department,
            "technology_stack": project.technology_stack,
            "duration_weeks": project.duration_weeks,
            "team_size": project.team_size,
            "guide_name": project.guide_name,
            "progress_percent": project.progress,
            "completed_milestones": project.milestones_completed,
            "total_milestones": project.total_milestones,
        },
        "blueprint": blueprint,
    }
    return chat_with_mentor(
        message=data.message,
        project_context=context,
        history=data.history,
    )


@router.post("/blueprint/preview", response_model=BlueprintResponse)
def preview_blueprint(
    data: BlueprintPreviewRequest,
):
    bp = project_service.preview_blueprint(data)
    return bp