from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class ProjectCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    idea: str = Field(min_length=10)
    student_name: str = "Student"
    student_email: str | None = None
    department: str | None = None
    academic_year: str | None = None

class ProjectUpdate(BaseModel):
    title: str | None = None
    idea: str | None = None
    status: Literal["planning", "in_progress", "blocked", "completed"] | None = None
    student_name: str | None = None
    student_email: str | None = None
    department: str | None = None
    academic_year: str | None = None

class MilestoneCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str | None = None
    due_date: str | None = None

class MilestoneUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    due_date: str | None = None
    status: Literal["pending", "in_progress", "completed", "blocked"] | None = None
    progress_percent: int | None = Field(default=None, ge=0, le=100)

class BlueprintRequest(BaseModel):
    project_id: int | None = None
    title: str = Field(min_length=2)
    idea: str = Field(min_length=10)
    academic_level: str = "Undergraduate"
    constraints: str | None = None

class ChatRequest(BaseModel):
    project_id: int | None = None
    message: str = Field(min_length=1, max_length=10000)

class DocumentRequest(BaseModel):
    project_id: int
    document_type: Literal["synopsis", "methodology", "progress_report"]
    extra_instructions: str | None = None

class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    idea: str
    student_name: str
    student_email: str | None
    department: str | None
    academic_year: str | None
    status: str
    blueprint_json: str | None
    created_at: datetime
    updated_at: datetime

class MilestoneOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    project_id: int
    title: str
    description: str | None
    due_date: str | None
    status: str
    progress_percent: int
    created_at: datetime
