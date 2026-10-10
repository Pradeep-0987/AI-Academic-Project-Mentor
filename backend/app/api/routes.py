import json
import secrets
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, func
from app.core.config import settings
from app.db.session import get_db
from app.db.models import Project, Milestone, MentorMessage, ProjectDocument
from app.schemas import (
    ProjectCreate, ProjectUpdate, ProjectOut, MilestoneCreate, MilestoneUpdate,
    MilestoneOut, BlueprintRequest, ChatRequest, DocumentRequest
)
from app.services.ai_service import generate_blueprint, mentor_reply, generate_document

router = APIRouter()

def require_faculty(authorization: str | None = Header(default=None)):
    token = settings.faculty_dashboard_token
    if not token:
        raise HTTPException(status_code=503, detail="Faculty dashboard token is not configured")
    expected = f"Bearer {token}"
    if not authorization or not secrets.compare_digest(authorization, expected):
        raise HTTPException(status_code=401, detail="Invalid faculty authorization")
    return True

@router.post("/projects", response_model=ProjectOut, status_code=201)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    item = Project(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.get("/projects", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.scalars(select(Project).order_by(Project.created_at.desc())).all()

@router.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    item = db.scalar(select(Project).options(selectinload(Project.milestones), selectinload(Project.documents)).where(Project.id == project_id))
    if not item:
        raise HTTPException(404, "Project not found")
    return {
        "id": item.id, "title": item.title, "idea": item.idea, "student_name": item.student_name,
        "student_email": item.student_email, "department": item.department, "academic_year": item.academic_year,
        "status": item.status, "blueprint_json": item.blueprint_json,
        "created_at": item.created_at, "updated_at": item.updated_at,
        "milestones": [MilestoneOut.model_validate(m).model_dump(mode="json") for m in item.milestones],
        "documents": [{"id": d.id, "document_type": d.document_type, "title": d.title, "created_at": d.created_at} for d in item.documents],
    }

@router.patch("/projects/{project_id}", response_model=ProjectOut)
def update_project(project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)):
    item = db.get(Project, project_id)
    if not item: raise HTTPException(404, "Project not found")
    for key, value in payload.model_dump(exclude_unset=True).items(): setattr(item, key, value)
    db.commit(); db.refresh(item)
    return item

@router.post("/projects/{project_id}/milestones", response_model=MilestoneOut, status_code=201)
def add_milestone(project_id: int, payload: MilestoneCreate, db: Session = Depends(get_db)):
    if not db.get(Project, project_id): raise HTTPException(404, "Project not found")
    item = Milestone(project_id=project_id, **payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.patch("/milestones/{milestone_id}", response_model=MilestoneOut)
def update_milestone(milestone_id: int, payload: MilestoneUpdate, db: Session = Depends(get_db)):
    item = db.get(Milestone, milestone_id)
    if not item: raise HTTPException(404, "Milestone not found")
    for key, value in payload.model_dump(exclude_unset=True).items(): setattr(item, key, value)
    if item.progress_percent == 100: item.status = "completed"
    db.commit(); db.refresh(item)
    return item

@router.post("/ai/generate-blueprint")
def blueprint(payload: BlueprintRequest, db: Session = Depends(get_db)):
    try:
        result = generate_blueprint(payload.title, payload.idea, payload.academic_level, payload.constraints)
    except RuntimeError as exc:
        raise HTTPException(503, str(exc))
    if payload.project_id:
        project = db.get(Project, payload.project_id)
        if not project: raise HTTPException(404, "Project not found")
        project.blueprint_json = json.dumps(result, ensure_ascii=False)
        db.commit()
    return {"blueprint": result}

@router.post("/mentor/chat")
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    project_context = ""
    if payload.project_id:
        project = db.get(Project, payload.project_id)
        if not project: raise HTTPException(404, "Project not found")
        project_context = f"Title: {project.title}; Idea: {project.idea}; Status: {project.status}"
    try:
        reply = mentor_reply(payload.message, project_context)
    except RuntimeError as exc:
        raise HTTPException(503, str(exc))
    db.add(MentorMessage(project_id=payload.project_id, role="user", message=payload.message))
    db.add(MentorMessage(project_id=payload.project_id, role="assistant", message=reply))
    db.commit()
    return {"reply": reply}

@router.post("/documents/generate", status_code=201)
def create_document(payload: DocumentRequest, db: Session = Depends(get_db)):
    project = db.get(Project, payload.project_id)
    if not project: raise HTTPException(404, "Project not found")
    try:
        content = generate_document(payload.document_type, project.title, project.idea, project.blueprint_json, payload.extra_instructions)
    except RuntimeError as exc:
        raise HTTPException(503, str(exc))
    doc = ProjectDocument(project_id=project.id, document_type=payload.document_type, title=f"{payload.document_type.replace('_',' ').title()} — {project.title}", content=content)
    db.add(doc); db.commit(); db.refresh(doc)
    return {"id": doc.id, "project_id": doc.project_id, "document_type": doc.document_type, "title": doc.title, "content": doc.content, "created_at": doc.created_at}

@router.get("/documents/projects/{project_id}")
def list_documents(project_id: int, db: Session = Depends(get_db)):
    if not db.get(Project, project_id): raise HTTPException(404, "Project not found")
    docs = db.scalars(select(ProjectDocument).where(ProjectDocument.project_id == project_id).order_by(ProjectDocument.created_at.desc())).all()
    return [{"id": d.id, "document_type": d.document_type, "title": d.title, "created_at": d.created_at} for d in docs]

@router.get("/documents/{document_id}")
def get_document(document_id: int, db: Session = Depends(get_db)):
    doc = db.get(ProjectDocument, document_id)
    if not doc: raise HTTPException(404, "Document not found")
    return {"id": doc.id, "project_id": doc.project_id, "document_type": doc.document_type, "title": doc.title, "content": doc.content, "created_at": doc.created_at}

@router.get("/faculty/dashboard")
def faculty_dashboard(_auth=Depends(require_faculty), db: Session = Depends(get_db)):
    total = db.scalar(select(func.count(Project.id))) or 0
    completed = db.scalar(select(func.count(Project.id)).where(Project.status == "completed")) or 0
    blocked = db.scalar(select(func.count(Project.id)).where(Project.status == "blocked")) or 0
    projects = db.scalars(select(Project).options(selectinload(Project.milestones)).order_by(Project.updated_at.desc())).all()
    items = []
    for p in projects:
        total_m = len(p.milestones)
        avg_progress = round(sum(m.progress_percent for m in p.milestones) / total_m) if total_m else 0
        items.append({"id": p.id, "title": p.title, "student_name": p.student_name, "department": p.department,
                      "status": p.status, "milestone_count": total_m, "progress_percent": avg_progress,
                      "updated_at": p.updated_at})
    return {"summary": {"total_projects": total, "completed_projects": completed, "blocked_projects": blocked,
                        "active_projects": total - completed}, "projects": items}

@router.get("/faculty/projects/{project_id}")
def faculty_project_detail(project_id: int, _auth=Depends(require_faculty), db: Session = Depends(get_db)):
    item = db.scalar(select(Project).options(selectinload(Project.milestones), selectinload(Project.documents)).where(Project.id == project_id))
    if not item: raise HTTPException(404, "Project not found")
    return {"project": ProjectOut.model_validate(item), "milestones": [MilestoneOut.model_validate(m) for m in item.milestones],
            "documents": [{"id": d.id, "title": d.title, "document_type": d.document_type, "created_at": d.created_at} for d in item.documents]}
