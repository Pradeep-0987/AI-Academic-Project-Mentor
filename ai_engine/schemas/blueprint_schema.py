from pydantic import BaseModel

from schemas.feasibility_schema import ProjectFeasibility
from schemas.scope_schema import ProjectScope
from schemas.technology_schema import TechnologyRecommendation
from schemas.planning_schema import ProjectPlan
from schemas.risk_schema import RiskAssessment
from schemas.research_schema import ResearchPlan
from schemas.dataset_schema import DatasetPlan
from schemas.architecture_schema import ArchitecturePlan
from schemas.testing_schema import EvaluationPlan
from schemas.documentation_schema import DocumentationPlan


class ProjectBlueprint(BaseModel):
    project_idea: str
    feasibility: ProjectFeasibility
    scope: ProjectScope
    technology: TechnologyRecommendation
    planning: ProjectPlan
    risk_assessment: RiskAssessment
    research: ResearchPlan
    dataset: DatasetPlan
    architecture: ArchitecturePlan
    testing: EvaluationPlan
    documentation: DocumentationPlan
