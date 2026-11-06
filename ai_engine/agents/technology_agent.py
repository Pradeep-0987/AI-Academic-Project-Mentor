import logging
from ai_engine.agents.common import generate_structured
from ai_engine.agents.heuristic_fallback import fallback_technology
from ai_engine.schemas import TechnologyResult

logger = logging.getLogger(__name__)


def recommend_technology(
    project_idea: str,
    feasibility: dict,
    scope: dict,
    skills: list[str] | None = None,
) -> TechnologyResult:
    prompt = f"""Act as a pragmatic academic software architect and technical mentor.
Recommend a tailored, modern, and production-ready technology stack that directly solves the requirements for: {project_idea.strip()}.
Include comprehensive reasoning output explaining the architectural rationale behind every selected technology layer and trade-offs against rejected alternatives.
Return JSON only matching this exact schema: {TechnologyResult.model_json_schema()}

CRITICAL TECH STACK & DOMAIN DIRECTIVES:
- Directly tailor the technology stack to the requirements of: {project_idea.strip()}
- If the project involves IoT, sensors, or edge devices, include appropriate protocols (MQTT, WebSockets), microcontrollers (ESP32, Raspberry Pi), and edge inference runtimes.
- If the project involves Computer Vision, include OpenCV, YOLOv8/PyTorch, Albumentations, and real-time streaming tools (WebRTC/MediaDevices).
- If the project involves Spatial/GIS data or Routing, include PostGIS, Leaflet/MapLibre, and Google OR-Tools / NetworkX.
- Alternatives must compare 3 genuine architectural alternatives with concrete technical rationales explaining why they were rejected for this specific project.
- The 'reasoning' field must detail the architectural justification for each tier in relation to the project's real-time performance and evaluation goals.

Sections to provide:
1. frontend: Modern UI frameworks and component libraries tailored to this system's interaction model
2. backend: High-performance API frameworks and language runtime
3. database: Primary relational / document / vector / time-series database suited for this data
4. ai_ml: Machine learning, deep learning, NLP, or computational libraries
5. deployment: Containerization and hosting platforms suitable for student budgets
6. development_tools: Testing, linting, CI/CD, and version control tools
7. alternatives: Competing technologies considered with concise rejection rationale
8. rationale: Overall summary rationale for the stack
9. reasoning: In-depth step-by-step reasoning explaining why each layer was chosen given the students' background and project requirements
10. limitations: Known operational constraints or hardware limitations of this stack

Idea: {project_idea.strip()}
Student Skills: {skills or []}
Feasibility Context: {feasibility}
Scope Context: {scope}"""

    try:
        res = generate_structured(prompt, TechnologyResult)
        if not res.reasoning:
            res.reasoning = res.rationale
        return res
    except Exception as exc:
        logger.warning(f"Technology agent live LLM call unavailable ({exc}); using domain-aware fallback.")
        return fallback_technology(project_idea, feasibility, scope, skills)
