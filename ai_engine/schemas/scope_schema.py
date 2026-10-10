
from pydantic import BaseModel, Field


class ProjectScope(BaseModel):
    project_title: str
    project_objective: str
    target_users: list[str]
    functional_requirements: list[str] = Field(min_length=3)
    non_functional_requirements: list[str]
    mvp_features: list[str] = Field(min_length=3)
    out_of_scope: list[str]
    deliverables: list[str]
    assumptions: list[str]
    success_criteria: list[str]
