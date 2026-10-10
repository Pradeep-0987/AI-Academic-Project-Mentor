from agents.base_agent import StructuredGeminiAgent
from schemas.documentation_schema import DocumentationPlan

class DocumentationAgent(StructuredGeminiAgent):
    schema = DocumentationPlan
    system_instruction = (
        "You are an academic technical writer and viva coach. Help students explain "
        "their own work honestly. Do not invent results, citations, or completed features."
    )

    def create_plan(self, project_idea: str, scope: str = "", architecture: str = "", testing: str = "") -> DocumentationPlan:
        return self.generate(
            "Create a report chapter outline, presentation slide outline, viva questions, "
            "answer guidance, demo checklist, and academic-integrity notes.",
            {"project_idea": project_idea, "scope": scope, "architecture": architecture, "testing": testing},
        )
