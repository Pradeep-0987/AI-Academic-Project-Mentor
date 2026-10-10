
from typing import Literal

from pydantic import BaseModel, Field


class ProjectFeasibility(BaseModel):
    project_title: str = Field(
        description="A concise title for the proposed project"
    )
    problem_statement: str = Field(
        description="The problem the project intends to solve"
    )
    feasibility: Literal["High", "Medium", "Low"]
    complexity: Literal["Beginner", "Intermediate", "Advanced"]
    required_skills: list[str]
    required_resources: list[str]
    potential_challenges: list[str]
    recommendations: list[str]
    reasoning: str = Field(
        description="Explain the feasibility assessment"
    )
