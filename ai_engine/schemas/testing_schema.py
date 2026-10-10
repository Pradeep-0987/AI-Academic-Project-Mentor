from pydantic import BaseModel, Field

class TestCase(BaseModel):
    test_name: str
    test_type: str
    steps: list[str] = Field(min_length=1)
    expected_result: str
    automation_candidate: bool

class EvaluationPlan(BaseModel):
    acceptance_criteria: list[str] = Field(min_length=3)
    test_cases: list[TestCase] = Field(min_length=3)
    evaluation_metrics: list[str] = Field(min_length=2)
    experiment_plan: list[str]
    evidence_required: list[str]
    summary: str
