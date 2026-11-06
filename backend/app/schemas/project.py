import uuid
from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

# Whitespace is trimmed first, then the length is checked,
# so a whitespace-only text fails the minimum length.
Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=200)]
Description = Annotated[str, StringConstraints(strip_whitespace=True, min_length=20, max_length=5000)]
Domain = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
Department = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]
TechnologyStack = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=1000)]
GuideName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]


class ProjectCreate(BaseModel):
    title: Title
    description: Description
    domain: Domain | None = None
    department: Department | None = None
    technology_stack: TechnologyStack | None = None
    duration_weeks: int = Field(default=8, ge=1, le=52)
    team_size: int | None = Field(default=None, ge=1, le=20)
    guide_name: GuideName | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_new_project_details(cls, value):
        if not isinstance(value, dict):
            return value
        required_fields = ("domain", "department", "technology_stack", "duration_weeks")
        if not any(field in value for field in required_fields):
            return value
        missing = [
            field for field in required_fields
            if field not in value or value[field] is None or (
                isinstance(value[field], str) and not value[field].strip()
            )
        ]
        if missing:
            raise ValueError(
                "New project submissions require domain, department, technology_stack, and duration_weeks."
            )
        return value


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str
    domain: str | None = None
    department: str | None = None
    technology_stack: str | None = None
    duration_weeks: int = 8
    team_size: int | None = None
    guide_name: str | None = None
    status: str
    created_at: datetime


class ProjectListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str | None = None
    domain: str | None = None
    department: str | None = None
    technology_stack: str | None = None
    duration_weeks: int = 8
    team_size: int | None = None
    guide_name: str | None = None
    progress: float = 0
    milestones_completed: int = 0
    total_milestones: int = 0
    delayed_milestones: int = 0
    next_deadline: str | None = None
    next_milestone: str | None = None
    status: str
    created_at: datetime


class BlueprintPreviewRequest(BaseModel):
    idea: str = Field(min_length=3, max_length=5000)
    duration_weeks: int = Field(default=8, ge=1, le=52)
    team_size: int | None = Field(default=None, ge=1, le=20)
    skills: list[str] = Field(default_factory=list)


class MentorChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    history: list[dict[str, str]] = Field(default_factory=list, max_length=20)


class MilestoneStatusUpdate(BaseModel):
    status: Literal["pending", "in_progress", "completed"]


class BlueprintResponse(BaseModel):
    project_id: uuid.UUID | None = None
    feasibility: dict[str, Any]
    scope: dict[str, Any]
    technology: dict[str, Any]
    planning: dict[str, Any]
    risk: dict[str, Any]
    quality_report: dict[str, Any]
    created_at: datetime | None = None