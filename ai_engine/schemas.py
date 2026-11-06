from typing import Literal
from pydantic import BaseModel, Field, ConfigDict

class StrictSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")

class FeasibilityResult(StrictSchema):
    project_title: str
    problem_statement: str
    feasibility: Literal["High", "Medium", "Low"]
    economic_feasibility: Literal["High", "Medium", "Low"] = "Medium"
    economic_reasoning: str = "Assess development, compute, deployment, and maintenance costs for the available budget."
    operational_feasibility: Literal["High", "Medium", "Low"] = "Medium"
    operational_reasoning: str = "Validate user workflows, adoption needs, and operational constraints before deployment."
    complexity: Literal["Beginner", "Intermediate", "Advanced"]
    required_skills: list[str]
    required_resources: list[str]
    potential_challenges: list[str]
    recommendations: list[str]
    assumptions: list[str]
    reasoning: str

class ScopeResult(StrictSchema):
    project_title: str
    project_objective: str
    proposed_solution: str = ""
    target_users: list[str]
    functional_requirements: list[str]
    non_functional_requirements: list[str]
    mvp_features: list[str]
    out_of_scope: list[str]
    deliverables: list[str]
    success_criteria: list[str]

class TechnologyResult(StrictSchema):
    frontend: list[str]
    backend: list[str]
    database: list[str]
    ai_ml: list[str]
    deployment: list[str]
    development_tools: list[str]
    alternatives: list[str]
    rationale: str
    limitations: list[str]
    reasoning: str | None = None

class PlannedPhase(StrictSchema):
    phase_name: str
    start_week: int = Field(ge=1)
    duration_weeks: int = Field(ge=1)
    tasks: list[str]
    deliverables: list[str]
    dependencies: list[str]

class WeeklyMilestone(StrictSchema):
    week_number: int = Field(ge=1)
    milestone_title: str
    objectives: list[str]
    tasks: list[str]
    deliverables: list[str]

class PlanningResult(StrictSchema):
    total_duration_weeks: int = Field(ge=1)
    phases: list[PlannedPhase]
    weekly_milestones: list[WeeklyMilestone] = Field(default_factory=list)

class ProjectRisk(StrictSchema):
    risk: str
    likelihood: Literal["Low", "Medium", "High"]
    impact: Literal["Low", "Medium", "High"]
    mitigation: str
    contingency_plan: str

class RiskResult(StrictSchema):
    risks: list[ProjectRisk]
