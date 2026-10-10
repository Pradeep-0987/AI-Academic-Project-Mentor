from agents.base_agent import StructuredGeminiAgent
from schemas.research_schema import ResearchPlan

class ResearchAgent(StructuredGeminiAgent):
    schema = ResearchPlan
    system_instruction = (
        "You are an academic research planning assistant. Never fabricate "
        "paper titles, authors, DOI numbers, or citations. Provide search "
        "queries and topics that a student can verify independently."
    )

    def create_plan(self, project_idea: str, scope: str = "") -> ResearchPlan:
        return self.generate(
            "Create a literature-review and research-gap plan. Suggested topics "
            "are not verified sources; clearly state that references must be checked.",
            {"project_idea": project_idea, "scope": scope},
        )
