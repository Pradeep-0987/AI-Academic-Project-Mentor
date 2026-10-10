
from pydantic import BaseModel, Field, field_validator


class PlanningPhase(BaseModel):
    phase_name: str
    duration_days: int
    tasks: list[str] = Field(min_length=1)
    deliverables: list[str] = Field(min_length=1)
    dependencies: list[str]

    @field_validator("duration_days")
    @classmethod
    def validate_duration(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Phase duration must be positive.")
        return value


class ProjectPlan(BaseModel):
    project_title: str
    total_duration_days: int
    phases: list[PlanningPhase] = Field(min_length=1)
    milestones: list[str] = Field(min_length=1)
    assumptions: list[str]
    schedule_risks: list[str]

    @field_validator("total_duration_days")
    @classmethod
    def validate_total_duration(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Total duration must be positive.")
        return value
