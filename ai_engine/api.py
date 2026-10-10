
import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from starlette.concurrency import run_in_threadpool

from workflows.blueprint_graph import generate_blueprint
from workflows.quality_checks import validate_blueprint_consistency


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
        "Generate academic project blueprints using five AI agents: "
        "feasibility, scope, technology, planning, and risk assessment."
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
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
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

        logger.info(
            "Blueprint generation completed. Quality warnings: %s",
            quality_report.get("warning_count", 0),
        )

        return {
            "success": True,
            "message": "Project blueprint generated successfully.",
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
