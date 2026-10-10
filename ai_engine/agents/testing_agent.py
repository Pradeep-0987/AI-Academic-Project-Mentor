from agents.base_agent import StructuredGeminiAgent
from schemas.testing_schema import EvaluationPlan

class TestingAgent(StructuredGeminiAgent):
    schema = EvaluationPlan
    system_instruction = (
        "You are a QA and evaluation engineer. Generate test plans, not test results. "
        "Do not mark tests as passed because no tests have been executed."
    )

    def create_plan(self, project_idea: str, scope: str = "", architecture: str = "") -> EvaluationPlan:
        return self.generate(
            "Create acceptance criteria, practical test cases, evaluation metrics, "
            "experiment steps, and evidence required to substantiate claims.",
            {"project_idea": project_idea, "scope": scope, "architecture": architecture},
        )
