
from typing import TypedDict


class BlueprintState(TypedDict, total=False):
    project_idea: str
    duration_weeks: int
    team_size: int

    feasibility: dict
    scope: dict
    technology: dict
    planning: dict
    risk_assessment: dict
