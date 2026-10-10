
import logging
import hmac
import os

from fastapi import FastAPI, HTTPException, Query, Header
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool

from mentor_service import (
    add_milestone, chat_with_mentor, create_project, get_project,
    list_projects, update_milestone,
    save_blueprint, list_blueprints, get_blueprint, get_project_progress,
)

from workflows.blueprint_graph import generate_blueprint
from workflows.quality_checks import validate_blueprint_consistency
from outcomes_service import (
    generate_document,
    list_documents,
    get_document,
    faculty_dashboard,
)


# --------------------------------------------------
# Logging
# --------------------------------------------------

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("academic_project_mentor")


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="AI Academic Project Mentor API",
    description=(
        "Generate academic project blueprints using ten AI agents covering "
        "feasibility, scope, technology, planning, risk, research, data, "
        "architecture, testing, and documentation."
    ),
    version="1.0.0",
)


# --------------------------------------------------
# CORS configuration for React frontend
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Accept", "Authorization"],
)


# --------------------------------------------------
# Request schema
# --------------------------------------------------

class BlueprintRequest(BaseModel):
    project_idea: str = Field(
        min_length=3,
        max_length=2000,
        description="The proposed academic project idea.",
    )

    duration_weeks: int = Field(
        default=8,
        ge=1,
        le=52,
        description="Available project duration in weeks.",
    )

    team_size: int = Field(
        default=6,
        ge=1,
        le=20,
        description="Number of project team members.",
    )


# --------------------------------------------------
# Health endpoints
# --------------------------------------------------

@app.get("/")
def health_check():
    return {
        "status": "running",
        "service": "AI Academic Project Mentor",
        "version": app.version,
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "AI Academic Project Mentor API",
    }


# --------------------------------------------------
# Blueprint generation endpoint
# --------------------------------------------------

@app.post("/api/ai/generate-blueprint")
async def create_blueprint(request: BlueprintRequest):
    logger.info(
        "Starting blueprint generation: duration=%s weeks, team_size=%s",
        request.duration_weeks,
        request.team_size,
    )

    try:
        # Run the synchronous LangGraph workflow without blocking
        # FastAPI's asynchronous event loop.
        blueprint = await run_in_threadpool(
            generate_blueprint,
            request.project_idea.strip(),
            request.duration_weeks,
            request.team_size,
        )

        # Convert the Pydantic blueprint to a JSON-compatible dict.
        blueprint_data = blueprint.model_dump(mode="json")

        # Validate the generated output using deterministic checks.
        quality_report = validate_blueprint_consistency(
            blueprint=blueprint_data,
            duration_weeks=request.duration_weeks,
        )

        saved = save_blueprint(
            project_idea=request.project_idea.strip(),
            duration_weeks=request.duration_weeks,
            team_size=request.team_size,
            blueprint=blueprint_data,
            quality_report=quality_report,
        )

        logger.info(
            "Blueprint generation completed and saved as ID %s. Quality warnings: %s",
            saved["id"],
            quality_report.get("warning_count", 0),
        )

        return {
            "success": True,
            "message": "Project blueprint generated and saved successfully.",
            "blueprint_id": saved["id"],
            "blueprint": blueprint_data,
            "quality_report": quality_report,
        }

    except ValueError as error:
        logger.exception("Blueprint validation error")

        raise HTTPException(
            status_code=422,
            detail=str(error),
        ) from error

    except Exception as error:
        logger.exception("Blueprint generation failed")

        raise HTTPException(
            status_code=502,
            detail=(
                "Blueprint generation failed. "
                "Check the backend terminal for the detailed error."
            ),
        ) from error


# --------------------------------------------------
# Conversational mentoring and progress tracking
# --------------------------------------------------

class MentorChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    project_id: int | None = Field(default=None, ge=1)
    history: list[dict] = Field(default_factory=list, max_length=20)


class ProjectCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    idea: str = Field(min_length=3, max_length=2000)
    target_date: str | None = Field(default=None, max_length=30)
    milestones: list[dict] = Field(default_factory=list, max_length=50)


class MilestoneCreateRequest(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str = Field(default="", max_length=2000)
    due_date: str | None = Field(default=None, max_length=30)


class MilestoneUpdateRequest(BaseModel):
    status: str | None = None
    title: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    due_date: str | None = Field(default=None, max_length=30)


@app.get("/api/mentor/projects")
def mentor_list_projects():
    return {"projects": list_projects()}


@app.post("/api/mentor/projects")
def mentor_create_project(request: ProjectCreateRequest):
    try:
        clean_milestones = []
        for item in request.milestones:
            if not isinstance(item, dict) or not str(item.get("title", "")).strip():
                raise ValueError("Each milestone must contain a non-empty title.")
            clean_milestones.append({
                "title": str(item["title"])[:200],
                "description": str(item.get("description", ""))[:2000],
                "due_date": item.get("due_date"),
                "status": "pending",
            })
        project = create_project(request.name.strip(), request.idea.strip(), request.target_date, clean_milestones)
        return {"success": True, "project": project}
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@app.get("/api/mentor/projects/{project_id}")
def mentor_get_project(project_id: int):
    project = get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    return {"project": project}


@app.post("/api/mentor/projects/{project_id}/milestones")
def mentor_add_milestone(project_id: int, request: MilestoneCreateRequest):
    milestone = add_milestone(project_id, request.title.strip(), request.description, request.due_date)
    if not milestone:
        raise HTTPException(status_code=404, detail="Project not found.")
    return {"success": True, "milestone": milestone}


@app.patch("/api/mentor/milestones/{milestone_id}")
def mentor_update_milestone(milestone_id: int, request: MilestoneUpdateRequest):
    try:
        milestone = update_milestone(
            milestone_id,
            status=request.status,
            title=request.title,
            description=request.description,
            due_date=request.due_date,
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found.")
    return {"success": True, "milestone": milestone}


@app.post("/api/mentor/chat")
async def mentor_chat(request: MentorChatRequest):
    try:
        result = await run_in_threadpool(
            chat_with_mentor,
            request.message.strip(),
            request.project_id,
            request.history,
        )
        return {"success": True, **result}
    except ValueError as error:
        raise HTTPException(status_code=404 if "not found" in str(error).lower() else 422, detail=str(error)) from error
    except Exception as error:
        logger.exception("Conversational mentor failed")
        raise HTTPException(status_code=502, detail="Mentor response failed. Check backend logs and Gemini API configuration.") from error


# --------------------------------------------------
# Outcome 3: On-demand academic documentation
# --------------------------------------------------

class DocumentGenerationRequest(BaseModel):
    project_id: int = Field(ge=1)
    document_type: str = Field(
        description="One of: synopsis, methodology, progress_report"
    )


@app.post("/api/documents/generate")
async def generate_project_document(request: DocumentGenerationRequest):
    if request.document_type not in {"synopsis", "methodology", "progress_report"}:
        raise HTTPException(
            status_code=422,
            detail="document_type must be synopsis, methodology, or progress_report.",
        )
    try:
        document = await run_in_threadpool(
            generate_document,
            request.project_id,
            request.document_type,
        )
        return {"success": True, "document": document}
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except Exception as error:
        logger.exception("Document generation failed")
        raise HTTPException(
            status_code=502,
            detail="Document generation failed. Check backend logs and Gemini configuration.",
        ) from error


@app.get("/api/documents/projects/{project_id}")
def get_project_documents(project_id: int):
    try:
        from mentor_service import get_project
        if not get_project(project_id):
            raise HTTPException(status_code=404, detail="Project not found.")
        return {"documents": list_documents(project_id)}
    except HTTPException:
        raise
    except Exception as error:
        logger.exception("Could not list project documents")
        raise HTTPException(status_code=500, detail="Could not list documents.") from error


@app.get("/api/documents/{document_id}")
def get_generated_document(document_id: int):
    document = get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")
    return {"document": document}


@app.get("/api/documents/{document_id}/download", response_class=PlainTextResponse)
def download_generated_document(document_id: int):
    document = get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")
    safe_name = "".join(
        ch if ch.isalnum() or ch in "-_" else "_" for ch in document["title"]
    )[:100]
    from fastapi.responses import Response
    return Response(
        content=document["content"],
        media_type="text/markdown; charset=utf-8",
        headers={"Content-Disposition": f'attachment; filename="{safe_name}.md"'},
    )


# --------------------------------------------------
# Outcome 4: Faculty dashboard (token-protected)
# --------------------------------------------------

def require_faculty_token(x_faculty_token: str | None):
    """Fail closed until a faculty dashboard token is configured in .env."""
    expected = os.getenv("FACULTY_DASHBOARD_TOKEN", "").strip()
    if not expected:
        raise HTTPException(
            status_code=503,
            detail="Faculty dashboard is disabled until FACULTY_DASHBOARD_TOKEN is configured.",
        )
    if not x_faculty_token or not hmac.compare_digest(x_faculty_token, expected):
        raise HTTPException(status_code=401, detail="Valid faculty token required.")


@app.get("/api/faculty/dashboard")
def get_faculty_dashboard(
    x_faculty_token: str | None = Header(default=None, alias="X-Faculty-Token"),
):
    require_faculty_token(x_faculty_token)
    try:
        return faculty_dashboard()
    except Exception as error:
        logger.exception("Faculty dashboard aggregation failed")
        raise HTTPException(status_code=500, detail="Could not load faculty dashboard.") from error


@app.get("/api/faculty/projects/{project_id}")
def get_faculty_project_detail(
    project_id: int,
    x_faculty_token: str | None = Header(default=None, alias="X-Faculty-Token"),
):
    require_faculty_token(x_faculty_token)
    dashboard = faculty_dashboard()
    project = next((item for item in dashboard["projects"] if item["id"] == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    return {"project": project}


# --------------------------------------------------
# Blueprint history and project progress
# --------------------------------------------------

@app.get("/api/blueprints")
def api_list_blueprints(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    try:
        return {"blueprints": list_blueprints(limit=limit, offset=offset)}
    except Exception as error:
        logger.exception("Could not list blueprints")
        raise HTTPException(status_code=500, detail="Could not list saved blueprints.") from error


@app.get("/api/blueprints/{blueprint_id}")
def api_get_blueprint(blueprint_id: int):
    try:
        blueprint = get_blueprint(blueprint_id)
        if not blueprint:
            raise HTTPException(status_code=404, detail="Blueprint not found.")
        return {"blueprint": blueprint}
    except HTTPException:
        raise
    except Exception as error:
        logger.exception("Could not retrieve blueprint")
        raise HTTPException(status_code=500, detail="Could not retrieve saved blueprint.") from error


@app.get("/api/mentor/projects/{project_id}/progress")
def api_project_progress(project_id: int):
    try:
        progress = get_project_progress(project_id)
        if not progress:
            raise HTTPException(status_code=404, detail="Project not found.")
        return {"progress": progress}
    except HTTPException:
        raise
    except Exception as error:
        logger.exception("Could not calculate project progress")
        raise HTTPException(status_code=500, detail="Could not calculate project progress.") from error
