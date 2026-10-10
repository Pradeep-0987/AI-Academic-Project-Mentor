
from typing import Literal

from pydantic import BaseModel, Field


class ProjectRisk(BaseModel):
    risk_title: str
    description: str
    category: str
    likelihood: Literal["Low", "Medium", "High"]
    impact: Literal["Low", "Medium", "High"]
    mitigation: list[str] = Field(min_length=1)
    contingency_plan: str
    owner_role: str


class RiskAssessment(BaseModel):
    project_title: str
    overall_risk_level: Literal["Low", "Medium", "High"]
    risks: list[ProjectRisk] = Field(min_length=1)
    recommendations: list[str]
    assumptions: list[str]
