from agents.base_agent import StructuredGeminiAgent
from schemas.dataset_schema import DatasetPlan

class DatasetAgent(StructuredGeminiAgent):
    schema = DatasetPlan
    system_instruction = (
        "You are a data engineering and dataset quality specialist. Recommend "
        "plausible sources and checks, but do not claim a dataset was downloaded "
        "or inspected unless actual data is provided."
    )

    def assess(self, project_idea: str, scope: str = "") -> DatasetPlan:
        return self.generate(
            "Recommend data requirements, dataset discovery approaches, columns, "
            "preprocessing, data quality checks, and leakage safeguards.",
            {"project_idea": project_idea, "scope": scope},
        )
