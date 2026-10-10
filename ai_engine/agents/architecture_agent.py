from agents.base_agent import StructuredGeminiAgent
from schemas.architecture_schema import ArchitecturePlan

class ArchitectureAgent(StructuredGeminiAgent):
    schema = ArchitecturePlan
    system_instruction = (
        "You are a software architect for student and prototype systems. "
        "Keep components consistent with the proposed scope and stack. Mermaid "
        "output must be a small valid flowchart, not a claim of implemented code."
    )

    def design(self, project_idea: str, scope: str = "", technology: str = "") -> ArchitecturePlan:
        return self.generate(
            "Design the system architecture, components, API contracts, data entities, "
            "data flow, security controls, and deployment approach.",
            {"project_idea": project_idea, "scope": scope, "technology": technology},
        )
