
from pydantic import BaseModel

from schemas.feasibility_schema import ProjectFeasibility
from schemas.scope_schema import ProjectScope
from schemas.technology_schema import TechnologyRecommendation
from schemas.planning_schema import ProjectPlan
from schemas.risk_schema import RiskAssessment


class ProjectBlueprint(BaseModel):
    project_idea: str
    feasibility: ProjectFeasibility
    scope: ProjectScope
    technology: TechnologyRecommendation
    planning: ProjectPlan
    risk_assessment: RiskAssessment
